#!/usr/bin/env python
# Simple debugger
# See instructions around line 85
import sys
import readline

# Our buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out
    
# main program that runs the buggy program
def main():
    print remove_html_markup('"<b>foo</b>"')

# globals
breakpoints = {}
watchpoints = {"quote": True}
watch_values = {}
stepping = True

"""
Our debug function
"""
def debug(command, my_locals):
    global stepping
    global breakpoints
    global watchpoints
    global watch_values
    
    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'):     # step
        stepping = True
        return True
    elif command.startswith('c'):   # continue
        stepping = False
        return True
    elif command.startswith('p'):    # print 
        if arg == None:
            print my_locals
        elif my_locals.has_key(arg):
            print arg, '=', repr(my_locals[arg])
        else:
            print "No such variable:", arg
        pass
    elif command.startswith('b'):    # breakpoint     
        try:
            arg = int(arg)
        except:
            pass
        if not isinstance(arg, int):
            print 'You must supply a line number'
        else:
            breakpoints[arg] = True
        pass
    elif command.startswith('w'):    # watch variable
        if arg == None:
            print 'You must supply a variable name'
        else:
            watchpoints[arg] = True
            try:
                watch_values[arg] = my_locals[arg]
            except:
                pass
        pass
    elif command.startswith('d'):    # delete watch/break point
        # YOUR CODE HERE
        arg1 = arg.split(' ')[0]
        arg2 = arg.split(' ')[1]
        if arg1 == "b":
            try:
                arg2 = int(arg2)
            except:
                pass
            if not isinstance(arg2, int):
                print 'Incorrect command'
            if breakpoints.has_key(arg2):
                breakpoints.pop(arg2)
            else:
                print "No such breakpoint defined", repr(arg2)
        elif arg1 == "w":
            if watchpoints.has_key(arg2):
                watchpoints.pop(arg2)
            else:
                print arg2, "is not defined as watchpoint"
        else:
            print "Incorrect command"
    elif command.startswith('q'):   # quit
        print "Exiting my-spyder..."
        sys.exit(0)
    else:
        print "No such command", repr(command)
        
    return False

commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"]

def input_command():
    # command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    #print command
    return command

"""
Our traceit function
Improve the traceit function to watch for variables in the watchpoint 
dictionary and print out (literally like that): 
event, frame.f_lineno, frame.f_code.co_name
and then the values of the variables, each in new line, in a format:
somevar ":", "Initialized"), "=>", repr(somevalue)
if the value was not set, and got set in the line, or
somevar ":", repr(old-value), "=>", repr(new-value)
when the value of the variable has changed.
If the value is unchanged, do not print anything.
"""
def traceit(frame, event, trace_arg):
    global stepping
    global breakpoints
    global watchpoints
    global watch_values

    watch_change = False
    if event == 'line':
        state = frame.f_locals
        watch_change = False
        for k in watchpoints:
            if k in state and k not in watch_values:
                watch_change = True
                print event, frame.f_lineno, frame.f_code.co_name
                print k, ": Initialized =>", repr(state[k])
                watch_values[k] = state[k]
            if k in state and k in watch_values:
                if state[k] != watch_values[k]:
                    watch_change = True
                    print event, frame.f_lineno, frame.f_code.co_name
                    print k, ":", repr(watch_values[k]), "=>", repr(state[k])
                    watch_values[k] = state[k]
        if watch_change:
            resume = False
            while not resume:
                command = input_command()
                resume = debug(command, frame.f_locals)
            
        if stepping or breakpoints.has_key(frame.f_lineno):
            print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
            resume = False
            while not resume:
                #print watchpoints
                #print frame.f_locals
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit

# Using the tracer
#sys.settrace(traceit)
#main()
#sys.settrace(None)

# with the commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"]
# the output should look like this (line numbers may be different):
#line 26 main {}
#line 10 remove_html_markup
#quote : Initialized => False
#line 13 remove_html_markup
#c : Initialized => '"'
#line 19 remove_html_markup
#quote : False => True
#line 13 remove_html_markup
#c : '"' => '<'
#line 21 remove_html_markup
#out : '' => '<'
#Exiting my-spyder...

sys.settrace(traceit)
main()
sys.settrace(None)
