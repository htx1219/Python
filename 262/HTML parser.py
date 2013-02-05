import sys
sys.path.append('/Users/HTX/Documents')

import ply.yacc as yacc
import ply.lex as lex
import htmltokens                 # use our JavaScript lexer
from htmltokens import tokens     # use out JavaScript tokens

start = 'html'    # the start symbol in our grammar, maybe 'js' sometimes

tag_stack = []

def p_html(p):
    'html : elt html'
    p[0] = [p[1]] + p[2]

def p_html_empty(p):
    'html : '
    p[0] = []

def p_elt_word(p):
    'elt : WORD'
    p[0] = ("word-element", p[1])

def p_elt_word_eq(p):
    'elt : EQUAL'
    p[0] = ("word-element", p[1])

def p_elt_word_string(p):
    'elt : STRING'
    p[0] = ('word-element',"``" + p[1] + "''")

def p_tagname(p):
    'tagname : WORD'
    global tag_stack
    tag_stack = [(p[1],p.lineno(1))] + tag_stack
    p[0] = p[1] 

def p_tagnameend(p):
    'tagnameend : WORD'
    global tag_stack 
    if (tag_stack[0])[0] != p[1]:
        print "HTML Syntax Error: <" + tag_stack[0][0] + "> on line " + str(tag_stack[0][1]) + " closed by </" + str(p[1]) + "> on line " + str(p.lineno(1))
        exit(1) 
    tag_stack = tag_stack[1:] 
    p[0] = p[1] 

def p_elt_tag_empty(p):
    # <br /> 
    'elt : LANGLE tagname tagargs SLASHRANGLE'
    global tag_stack 
    tag_stack = tag_stack[1:] 
    p[0] = ('tag-element',p[2],p[3],[],p[2]) 

##def p_elt_number(p):
##    'elt : NUMBER'
##    p[0] = ("word-element", p[1])

def p_elt_tag(p):
    'elt : LANGLE tagname tagargs RANGLE html LANGLESLASH tagnameend RANGLE'
    p[0] = ("tag_element", p[2], p[3], p[5], p[7])

def p_tagargs_empty(p):
    'tagargs : '
    p[0] = { }

def p_tagargs(p):
    'tagargs : tagarg tagargs'
    p[0] = dict(p[1].items() + p[2].items())

def p_tagarg(p):
    'tagarg : WORD EQUAL STRING'
    p[0] = { p[1].lower(): p[3] }

def p_elt_javascript(p):
    'elt : JAVASCRIPT'
    p[0] = ("javascript-element", p[1])

##def p_error(t):
##    if tag_stack[0] != []:
##        print "HTML Syntax Error: <" + tag_stack[0][0] + "> on line " + str(tag_stack[0][1]) + " never closed" 
##    else:
##        tok = yacc.token()
##        print "HTML Syntax Error: Near Token " + str(tok)
##        exit(1) 

htmllexer = lex.lex(module=htmltokens) 
htmlparser = yacc.yacc() 

def test_lexer(input_string):
  htmllexer.input(input_string)
  result = [ ] 
  while True:
    tok = htmllexer.token()
    if not tok: break
    result = result + [tok.type]
  return result

def test_parser(input_string):
    htmllexer.input(input_string)
    parse_tree = htmlparser.parse(input_string,lexer=htmllexer)
    return parse_tree

# Simple function with no arguments and a one-statement body.
htmltext3 = """<html>
<h1>The Zinc Chef</h1>
<p>
I learned everything like 1 24 365 I know from 
<a href = "http://udacity.com/cs101x/urank/nickel.html" q = 'nimade'>the Nickel Chef</a>.
</p>
</html>
"""

htmltext2 = '<a href = "http://udacity.com/cs101x/urank/nickel.html" q = "nimei">the Nickel Chef</a>'

htmltext1 = '<html> hello my <script type="text/javascript">document.write(99);</script> loftballons </html>'
print test_lexer(htmltext1)
print test_parser(htmltext1)
