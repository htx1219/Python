import re
import ply.lex as lex

tokens = (
    'LANGLESLASH',
    'LANGLE',
    'RANGLE',
    'EQUAL',
    'STRING',
    'NUMBER',
    'WORD',
)

t_ignore = ' '
t_htmlcomment_ignore = ' \t\v\r'

states = (
    ('htmlcomment', 'exclusive'),
)

def t_htmlcomment(token):
    r'<!--'
    token.lexer.begin('htmlcomment')

def t_htmlcomment_end(token):
    r'-->'
    token.lexer.lineno += token.value.count('\n')
    token.lexer.begin('INITIAL')

def t_htmlcomment_error(token):
    token.lexer.skip(1)
    
def t_LANGLESLASH(token):
    r'</'
    return token

def t_LANGLE(token):
    r'<'
    return token

def t_RANGLE(token):
    r'>'
    return token

def t_EQUAL(token):
    r'='
    return token

def t_newline(token):
    r'\n'
    token.lexer.lineno += 1
    pass
"""
def t_WIHTESPACE(token):
    r" "
    pass
"""

def t_eolcomment(token):
    r'//[^\n]*'
    pass

def t_STRING(token):
    r'"[^"]*"'
    token.value = token.value[1:-1]
    return token

def t_NUMBER(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

def t_WORD(token):
    r'[^ <>\n]+'
    return token

##def t_IDENTIFIER(token):
##    r'[a-zA-Z][a-zA-Z_]*'
##    return token

def t_error(t):
    t.lexer.skip(1)

webpage = """This is <b>ab<!-- a comment
right?-->a
webpage!</b>
 
 """
htmllexer = lex.lex()
htmllexer.input(webpage)
##while True:
##    tok = htmllexer.token()
##    if not tok: break
##    print tok
