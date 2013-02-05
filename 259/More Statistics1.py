#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# The provided code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the provided code
# to work also on function calls (you can use your code from problem set 5 here)
# Use the mystery function that can be found at line 170 and the
# test cases at line 165 for this exercise.
# Remember that for functions the phi values have to be calculated as
# described in the problem set 5 video - 
# you should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
#
# Then combine both approaches to find out the function call and its return
# value that is the most correlated with failure, and then - the line in the
# function. Calculate phi values for the function and the line and put them
# in the variables below. 
# Do NOT set these values dynamically.

answer_function = "f5"   # One of f1, f2, f3
answer_bin = 42          # One of 1, 0, -1
answer_function_phi = 42.0000    # precision to 4 decimal places.
answer_line_phi = 42.0000 # precision to 4 decimal places.
# if there are several lines with the same phi value, put them in a list,
# no leading whitespace is required
answer_line = ["if False:", 'return "FAIL"']  # lines of code


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
        if filename in ["f1", "f2", "f3"]:
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

# These are the test cases for the remove_html_input function          
inputs_line = ['foo', 
          '<b>foo</b>', 
          '"<b>foo</b>"', 
          '"foo"', 
          "'foo'", 
          '<em>foo</em>', 
          '<a href="foo">foo</a>',
          '""',
          "<p>"]     
            
# These are the input values you should test the mystery function with
inputs = ["aaaaa223%", "aaaaaaaatt41@#", "asdfgh123!", "007001007", "143zxc@#$ab", "3214&*#&!(", "qqq1dfjsns", "12345%@afafsaf"]

###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == str
    assert len(magic) > 0
    
    r1 = f1(magic)
    
    r2 = f2(magic)
    
    r3 = f3(magic)
    
    print magic, r1, r2, r3

    if r1 < 0 or r3 < 0:
        return "FAIL"
    elif (r1 + r2 + r3) < 0:
        return "FAIL"
    elif r1 == 0 and r2 == 0:
        return "FAIL"
    else:
        return "PASS"


def f1(ml):
    if len(ml) <6:
        return -1
    elif len(ml) > 12 :
        return 1
    else:
        return 0
    
def f2(ms):
    digits = 0
    letters = 0
    for c in ms:
        if c in "1234567890":
            digits += 1
        elif c.isalpha():
            letters += 1
    other = len(ms) - digits - letters
    grade = 0
    
    if (other + digits) > 3:
        grade += 1 
    elif other < 1:
        grade -= 1
           
    return grade

def f3(mn):
    forbidden = ["pass", "123", "qwe", "111"]
    grade = 0
    for word in forbidden:
        if mn.find(word) > -1:
            grade -= 1
    if mn.find("%") > -1:
        grade += 1
    return grade

runs = run_tests(inputs)

tables = init_tables(runs)

tables = compute_n(tables, runs)

print_tables(tables) 
