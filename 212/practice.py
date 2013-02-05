import re
def count_words(passage):
    words = re.findall(r'[^ \n]+', passage)
    return len(words)


passage ='''The number of orderings of the 52 cards in a deck of cards
is so great that if every one of the almost 7 billion people alive
today dealt one ordering of the cards per second, it would take
2.5 * 10**40 times the age of the universe to order the cards in every
possible way.'''
print count_words(passage)

speed_of_light = 300000. # km per second

def speed_fraction(time, distance):
    return (distance*2.0*1000/time)/speed_of_light

print speed_fraction(50,5000)
#>>> 0.666666666667

print speed_fraction(50,10000)

def convert_seconds(t):
    h = int(t)/3600
    left = t%3600
    m = int(left)/60
    s = left%60
    q = [str(h), 'hour,' if h == 1 else 'hours,', str(m), 'minute,' if m==1 else 'minutes,',str(s), 'second' if s==1 else 'seconds']
    return ' '.join(q)

print convert_seconds(3661)
#>>> 1 hour, 1 minute, 1 second

print convert_seconds(7325)
#>>> 2 hours, 2 minutes, 5 seconds

print convert_seconds(7261.7)
#>>> 2 hours, 1 minute, 1.7 seconds

def download_time(fsize, funit, bwidth, bunit):
    unit = {'kb': 2**10, 'kB': 2**10*8, 'Mb':2**20, 'MB':2**20*8, 'Gb': 2**30, 'GB': 2**30*8, 'Tb': 2**40, 'TB':2**40*8}
    t = fsize*1.0*unit[funit] / (bwidth*unit[bunit])
    return convert_seconds(t)



print download_time(1024,'kB', 1, 'MB')
#>>> 0 hours, 0 minutes, 1 second

print download_time(1024,'kB', 1, 'Mb')
#>>> 0 hours, 0 minutes, 8 seconds  # 8.0 seconds is also acceptable

print download_time(13,'GB', 5.6, 'MB')
#>>> 0 hours, 39 minutes, 37.1428571429 seconds

print download_time(13,'GB', 5.6, 'Mb')
#>>> 5 hours, 16 minutes, 57.1428571429 seconds

print download_time(10,'MB', 2, 'kB')
#>>> 1 hour, 25 minutes, 20 seconds  # 20.0 seconds is also acceptable

print download_time(10,'MB', 2, 'kb')
#>>> 11 hours, 22 minutes, 40 seconds  # 40.0 seconds is also acceptable


# Introducing Your Web Browser 
#
#
# Although we have not put our HTML interpreter and our JavaScript
# interpreter together yet, we can still render HTML-only web pages. 
#
# A critical concept in interpreting HTML is proper tag nesting. 
#
# In this exercise you will learn a bit of HTML on your own and construct
# properly nested, simple HTML that renders to match the reference image we
# have provided. You do not have to match the exact text shown, but you do
# have to match the order and nesting of the tags used. 
#
# See the rendering image for reference output.
#
# In class we have discussed a few HTML tags, such as <b>, <i>, 
# <a href="http://www.udacity.com">, and <p>. It turns out, there are many
# more. In this exercise you will reverse-engineer some HTML tags you may
# not have seen before. Explicitly teaching you the various HTML tags is
# not a focus of this course, but you now know enough to learn them 
# easily on your own.
#
# Complete the webpage string below with HTML that renders an image similar
# to the reference. You must match the tag ordering and nesting, but you
# can change the text. 
#
# The reference image explicitly names every HTML tag it uses (it puts them
# in parentheses instead of angle brackets). If you would like a bit of a
# challenge, you can infer everything from that image alone. However, you
# are also encouraged to use any external source or HTML tutorial you would
# like. For example, these may help you brush up: 
# 
# http://www.w3schools.com/html/html_primary.asp
# http://www.w3schools.com/html/html_elements.asp
# http://www.w3schools.com/html/html_headings.asp
# http://www.w3schools.com/html/html_lists.asp 
# http://www.w3schools.com/html/html_images.asp
#
# Hint 1: The most common error is <b> opening one tag then </u> closing
# another. For our web browser, even tags like <p>, <li> and <img> must be
# properly closed! (Real-world web browsers are more forgiving, but one
# purpose of this exercise is to master properly nested tags.)
#
# Hint 2: Unlike <a href=...>my text</a>, do not put any text inside 
# <img src=...></img>. Just close it immediately. 

webpage = """<html>
<h1>Level One Headings Use (H1) Tags</h1> 
<p>Paragraphs use (P) tags. Unordered lists use (UL) tags.
<ul>
  <li> List items use (LI) tags. </li> 

  <!-- You should update this HTML until the order and nesting of
       the tags match the reference image. --> 

</ul>
</p> 
</html> 
"""

# Display the page!

import ply.lex as lex
import ply.yacc as yacc
import htmltokens
import htmlgrammar
import htmlinterp
import graphics as graphics
import jstokens


htmllexer = lex.lex(module=htmltokens) 
htmlparser = yacc.yacc(module=htmlgrammar,tabmodule="parsetabhtml") 
ast = htmlparser.parse(webpage,lexer=htmllexer) 
jslexer = lex.lex(module=jstokens) 
graphics.initialize() # Enables display of output.
htmlinterp.interpret(ast) 
graphics.finalize() # Enables display of output.

# "I Could Wile Away The Hours"
#
# 
# Although our HTML and JavaScript interpreters are not yet integrated into
# a single browser, we can still extend our JavaScript interpreter
# independently. We already have support for recursive functions and "if"
# statements, but it would be nice to add support for "while".
#
# Consider the following two JavaScript fragments:
#
#    var i = 0;
#    while (i <= 5) {
#      document.write(i); 
#      i = i + 2;
#    };
#
# And: 
#
#    function myloop(i) {
#      if (i <= 5) {
#         document.write(i);
#         myloop(i + 2);
#      } ;
#    } 
#    myloop(0);
#
# They both have the same effect: they both write 0, 2 and 4 to the
# webpage. (In fact, while loops and recursion are equally powerful! You
# really only need one in your language, but it is very convenient to have
# them both.) 
#
# We can extend our lexer to recognize 'while' as a keyword. We can extend
# our parser with a new statement rule like this: 
#
#    def p_stmt_while(p):
#        'stmt : WHILE exp compoundstmt'
#         p[0] = ("while",p[2],p[3])
#
# Now we just need to extend our interpreter to handle while loops. The
# meaning of a while loop is: 
#
#       1. First, evaluate the conditional expression in the current
#       environment. If it evaluates to false, stop.
#
#       2. Evaluate the body statements in the current environment. 
#
#       3. Go to step 1. 
#
# Recall that our JavaScript interpreter might have functions like:
#
#       eval_stmts(stmts,env)
#       eval_stmt(stmt,env)
#       eval_exp(exp,env) 
#
# For this assignment, you should write a procedure:
#
#       eval_while(while_stmt,evn) 
#
# Your procedure can (and should!) call those other procedures. Here is 
# how our interpreter will call your new eval_while(): 
# 
# def eval_stmt(stmt,env): 
#         stype = stmt[0] 
#         if stype == "if-then":
#                 cexp = stmt[1]
#                 then_branch = stmt[2] 
#                 if eval_exp(cexp,env):
#                         eval_stmts(then_branch,env) 
#         elif stype == "while":
#                 eval_while(stmt,env) 
#         elif stype == "if-then-else":
#                 ...
#
# Hint 1: We have structured this problem so that it is difficult for you
# to test (e.g., because we have not provided you the entire JavaScript
# interpreter framework). Thus, you should think carefully about how to
# write the code correctly. Part of the puzzle of this exercise is to
# reason to the correct answer without "guess and check" testing.
#
# Hint 2: It is totally legal to define JavaScript's while using a Python
# while statement. (Remember, an interpreter is like a translator.) You
# could also define JavaScript's while using recursion in Python.
#
# Hint 3: Extract the conditional expression and while loop body statements
# from while_stmt first. 

def eval_while(while_stmt, exp):
        # Fill in your own code here. Can be done in as few as 4 lines.



# Higher-Order Functions
#
# Back in Unit 3 we introduced Python List Comprehensions -- a concise
# syntax for specifying a new list in terms of a transformation of an old
# one.
#
# For exmaple:
#
# numbers = [1,2,3,4,5]
# odds = [n for n in numbers if n % 2 == 1] 
# squares = [n * n for n in numbers] 
#
# That code assigns [1,3,5] to odds and [1,4,9,16,25] to squares. The first
# operation is sometimes called "filter" (because we are filtering out
# unwanted elements) and the second operation is sometimes called "map"
# (because we are mapping, or transforming, all of the elements in a list). 
#
# Python also has functions behave similarly: 
#
# odds = filter(lambda n : n % 2 == 1, numbers) 
# squares = map(lambda n : n * n, numbers) 
#
# The filter() and map() definitions for odds and squares produce the same
# results as the list comprehension approaches. In other words, we can
# define (or implement) list comprehensions in terms of map and filter. 
#
# In this exercise we take that notion one step beyond, by making
# specialized maps and filters. For example, suppose that we know that we
# will be filtering many lists down to only their odd elements. Then we
# might want something like this:
#
# filter_odds = filter_maker(lambda n : n % 2 == 1)
# odds = filter_odds(numbers) 
#
# In this example, "filter_maker()" is a function that takes a function as
# an argument and returns a function as its result. We say that
# filter_maker is a *higher order function*. 
#
# Complete the code below with definitions for filter_maker() and
# map_maker(). 
#
# Hint: You can use either "lambda" or nested Python function definitions.
# Both will work. The function you return from filter_maker(f) will have to
# reference f, so you'll want to think about nested environments.

def filter_maker(f):
        # Fill in your code here. You must return a function.

def map_maker(f):
        # Fill in your code here. You must return a function.

# We have included a few test cases. You will likely want to add your own.
numbers = [1,2,3,4,5,6,7]
filter_odds = filter_maker(lambda n : n % 2 == 1) 
print filter_odds(numbers) == [1,3,5,7]
        
length_map = map_maker(len) 
words = "Scholem Aleichem wrote Tevye the Milkman, which was adapted into the musical Fiddler on the Roof.".split() 
print length_map(words) == [7, 8, 5, 5, 3, 8, 5, 3, 7, 4, 3, 7, 7, 2, 3, 5]

string_reverse_map = map_maker(lambda str : str[::-1]) 
# str[::-1] is cute use of the Python string slicing notation that 
# reverses str. A hidden gem in the homework!
print string_reverse_map(words) == ['melohcS', 'mehcielA', 'etorw', 'eyveT', 'eht', ',namkliM', 'hcihw', 'saw', 'detpada', 'otni', 'eht', 'lacisum', 'relddiF', 'no', 'eht', '.fooR']

square_map = map_maker(lambda n : n * n) 
print [n*n for n in numbers if n % 2 == 1] == square_map(filter_odds(numbers))
