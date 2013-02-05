#!/usr/bin/env python
# INSTRUCTIONS
# Your task for this assignment is to combine the principles that you learned 
# in unit 3, 4 and 5 and create a fully automated program that can display
# the cause-effect chain automatically.
# In problem set 4 you created a program that generated cause chain
# if you provided it the locations (line and iteration number) to look at.
# That is not very useful. If you know the lines to look for changes, you
# already know a lot about the cause. Instead now, with the help of concepts
# introduced in unit 5 (line coverage), improve this program to create
# the locations list automatically, and then use it to print out only the
# failure inducing lines, as before.
# See some hints at the provided functions, and an example output at the end.
import sys
import copy

#buggy program
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
    
def ddmin(s):
    # you may need to use this to test if the values you pass actually make
    # test fail.
    assert test(s) == "FAIL"

    n = 2     # Initial granularity
    while len(s) >= 2:
        start = 0
        subset_length = len(s) / n
        some_complement_is_failing = False

        while start < len(s):
            complement = s[:start] + s[start + subset_length:]

            if test(complement) == "FAIL":
                s = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break
                
            start += subset_length

        if not some_complement_is_failing:
            if n == len(s):
                break
            n = min(n * 2, len(s))

    return s


# Use this function to record the covered lines in the program, in order of
# their execution and save in the list coverage
coverage = []
def traceit(frame, event, arg):
    global coverage

    # YOUR CODE HERE
    if event == "line":
        lineno   = frame.f_lineno
        coverage.append(lineno)
        
    return traceit

# We use these variables to communicate between callbacks and drivers
the_line      = None
the_iteration = None
the_state     = None
the_diff      = None
the_input     = None

# Stop at THE_LINE/THE_ITERATION and store the state in THE_STATE
def trace_fetch_state(frame, event, arg):
    global the_line
    global the_iteration
    global the_state

    if frame.f_lineno == the_line:
        the_iteration = the_iteration - 1
        if the_iteration == 0:
            the_state = copy.deepcopy(frame.f_locals)
            the_line = None  # Don't get called again
            return None      # Don't get called again

    return trace_fetch_state

# Get the state at LINE/ITERATION
def get_state(input, line, iteration):
    global the_line
    global the_iteration
    global the_state
    
    the_line      = line
    the_iteration = iteration
    sys.settrace(trace_fetch_state)
    y = remove_html_markup(input)
    sys.settrace(None)
    
    return the_state

# Stop at THE_LINE/THE_ITERATION and apply the differences in THE_DIFF 
def trace_apply_diff(frame, event, arg):
    global the_line
    global the_diff
    global the_iteration

    if frame.f_lineno == the_line:
        the_iteration = the_iteration - 1
        if the_iteration == 0:
            frame.f_locals.update(the_diff)
            the_line = None
            return None  # Don't get called again
    
    return trace_apply_diff
    
# Testing function: Call remove_html_output, stop at THE_LINE/THE_ITERATION, 
# and apply the diffs in DIFFS at THE_LINE
def test(diffs):
    global the_diff
    global the_input
    global the_line
    global the_iteration

    line      = the_line
    iteration = the_iteration
    
    the_diff = diffs
    sys.settrace(trace_apply_diff)
    y = remove_html_markup(the_input)
    sys.settrace(None)

    the_line      = line
    the_iteration = iteration

    if y.find('<') == -1:
        return "PASS"
    else:
        return "FAIL"

def make_locations(coverage):
    # YOUR CODE HERE
    # This function should return a list of tuples in the format
    # [(line, iteration), (line, iteration) ...], as auto_cause_chain
    # expects.
    locations = []
    iteration = 1
    p_l = 0
    for i in coverage:
        if i < p_l:
            iteration += 1
        p_l = i
        locations.append((i, iteration))
    return locations

def auto_cause_chain(locations):
    global html_fail, html_pass, the_input, the_line, the_iteration, the_diff
    print "The program was started with", repr(html_fail)

    precause = None
    # Test over multiple locations
    for (line, iteration) in locations:

        # Get the passing and the failing state
        state_pass = get_state(html_pass, line, iteration)
        state_fail = get_state(html_fail, line, iteration)
    
        # Compute the differences
        diffs = []
        for var in state_fail.keys():
            if not state_pass.has_key(var) or state_pass[var] != state_fail[var]:
                diffs.append((var, state_fail[var]))
 
        # Minimize the failure-inducing set of differences
        # Since this time you have all the covered lines and iterations in
        # locations, you will have to figure out how to automatically detect
        # which lines/iterations are the ones that are part of the
        # failure chain and print out only these.
        the_input = html_pass
        the_line  = line
        the_iteration  = iteration
        # You will have to use the following functions and output formatting:
        try:
            cause = ddmin(diffs)
        #    # Pretty output
            
            for (var, value) in cause:
                if precause == None:
                    print "Then", var, "became", repr(value)
                elif  (var, value) not in precause:
                    print "Then", var, "became", repr(value)
            precause = copy.deepcopy(cause)
        except:
            pass
            
    print "Then the program failed."

###### Testing runs

# We will test your function with different strings and on a different function      
html_fail = '"<b>foo</b>"'
html_pass = "'<b>foo</b>'"

html_fail = '"<'
html_pass = "'<"
# This will fill the coverage variable with all lines executed in a
# failing run
coverage = []
sys.settrace(traceit)
remove_html_markup(html_fail)
sys.settrace(None)

locations = make_locations(coverage)
auto_cause_chain(locations)

# The coverage :
# [8, 9, 10, 11, 12, 14, 16, 17, 11, 12... # and so on
# The locations:
# [(8, 1), (9, 1), (10, 1), (11, 1), (12, 1)...  # and so on
# The output for the current program and test strings should look like follows:
"""
The program was started with '"<b>foo</b>"'
Then s became '"<b>foo</b>"'
Then c became '"'
Then quote became True
...
"""
