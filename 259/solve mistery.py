#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# This provided, working code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the traceit 
# function to work for function calls instead of lines. It should save the 
# function name and the return value of the function for each function call. 
# Use the mystery function that can be found at line 155 and the
# test cases at line 180 for this exercise.
# Modify the provided functions to use this information to calculate
# phi values for the function calls as described in the video.
# You should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
# When you have found out which function call and which return value type (bin)
# correlates the most with failure, fill in the following 3 variables,
# Do NOT set these values dynamically.

answer_function = "X"   # One of f1, f2, f3
answer_bin = 42         # One of 1, 0, -1
answer_value = 1.0000   # precision to 4 decimal places.

# The buggy program
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


# global variable to keep the coverage data in
return_values = {}
# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in 
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
def traceit(frame, event, arg):
    global return_values

    if event == "return":
        filename = frame.f_code.co_name
        lineno   = frame.f_lineno
        if not return_values.has_key(filename):
             return_values[filename] = []
        return_values[filename].append(arg)
        
    return traceit

# Calculate phi coefficient from given values            
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) / 
             math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))

# Print out values of phi, and result of runs for each covered line
def print_tables(tables):
    for filename in tables.keys():
        for i in [-1, 0, 1]: # lines of the remove_html_markup in this file
            if tables[filename].has_key(i):
                (n11, n10, n01, n00) = tables[filename][i]
                try:
                    factor = phi(n11, n10, n01, n00)
                    prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
                except:
                    prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
                    
            else:
                prefix = "               "
                    
            print prefix, [" 0", " 1", "-1"][i], filename
                            
# Run the program with each test case and record 
# input, outcome and coverage of lines
def run_tests(inputs):
    runs   = []
    for input in inputs:
        global return_values
        return_values = {}
        sys.settrace(traceit)
        outcome = mystery(input)
        sys.settrace(None)
        
        runs.append((input, outcome, return_values))
    return runs

# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for filename, rets in return_values.iteritems():
            for i in [-1,0, 1]:
                if not tables.has_key(filename):
                    tables[filename] = {}
                if not tables[filename].has_key(i):
                    tables[filename][i] = (0, 0, 0, 0)

    return tables

# Compute n11, n10, etc. for each line
def compute_n(tables, runs):
    for filename, iters in tables.iteritems():
        for i in [-1, 0, 1]:
            (n11, n10, n01, n00) = tables[filename][i]
            for (input, outcome, rets) in runs:
                ret = rets[filename][0]
                if i == -1:
                    if outcome == "FAIL":
                        if ret < 0:
                            n11 += 1
                        else:
                            n01 += 1
                    else:
                        if ret < 0:
                            n10 += 1
                        else:
                            n00 += 1
                elif i ==0:
                    if outcome == "FAIL":
                        if ret == 0:
                            n11 += 1
                        else:
                            n01 += 1
                    else:
                        if ret == 0:
                            n10 += 1
                        else:
                            n00 += 1
                elif i==1:
                    if outcome == "FAIL":
                        if ret > 0:
                            n11 += 1
                        else:
                            n01 += 1
                    else:
                        if ret > 0:
                            n10 += 1
                        else:
                            n00 += 1
            tables[filename][i] = (n11, n10, n01, n00)
    return tables
      
# Now compute (and report) phi for each line. The higher the value,
# the more likely the line is the cause of the failures.

# These are the test cases          
inputs_line = ['foo', 
          '<b>foo</b>', 
          '"<b>foo</b>"', 
          '"foo"', 
          "'foo'", 
          '<em>foo</em>', 
          '<a href="foo">foo</a>',
          '""',
          "<p>"]     
            
###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == tuple
    assert len(magic) == 3
    
    l, s, n = magic
    
    r1 = f1(l)
    
    r2 = f2(s)
    
    r3 = f3(n)

    if -1 in [r1, r2, r3]:
        return "FAIL"
    elif r3 < 0:
        return "FAIL"
    elif not r1 or not r2:
        return "FAIL"
    else:
        return "PASS"


# These are the input values you should test the mystery function with
inputs = [([1,2],"ab", 10), 
          ([1,2],"ab", 2),
          ([1,2],"ab", 12),
          ([1,2],"ab", 21),
          ("a",1, [1]),
          ([1],"a", 1),
          ([1,2],"abcd", 8),
          ([1,2,3,4,5],"abcde", 8),
          ([1,2,3,4,5],"abcdefgijkl", 18),
          ([1,2,3,4,5,6,7],"abcdefghij", 5)]

def f1(ml):
    if type(ml) is not list:
        return -1
    elif len(ml) <6 :
        return len(ml)
    else:
        return 0
    
def f2(ms):    
    if type(ms) is not str:
        return -1
    elif len(ms) <6 :
        return len(ms)
    else:
        return 0

def f3(mn):
    if type(mn) is not int:
        return -1
    if mn > 10:
        return -100
    else:
        return mn

runs = run_tests(inputs)

tables = init_tables(runs)

tables = compute_n(tables, runs)

print_tables(tables) 
