import ply.lex as lex

def test_lexer(lexer,input_string):
  lexer.input(input_string)
  result = [ ] 
  while True:
    tok = lexer.token()
    if not tok: break
    result = result + [tok.type]
  return result
  
tokens = (
        'ANDAND',       # &&
        'COMMA',        # ,
        'DIVIDE',       # /
        'ELSE',         # else
        'EQUAL',        # =
        'EQUALEQUAL',   # ==
        'FALSE',        # false
        'FUNCTION',     # function
        'GE',           # >=
        'GT',           # >
        'IDENTIFIER',   #### Not used in this problem.
        'IF',           # if
        'LBRACE',       # {
        'LE',           # <=
        'LPAREN',       # (
        'LT',           # <
        'MINUS',        # -
        'NOT',          # !
        'NUMBER',       #### Not used in this problem.
        'OROR',         # ||
        'PLUS',         # +
        'RBRACE',       # }
        'RETURN',       # return
        'RPAREN',       # )
        'SEMICOLON',    # ;
        'STRING',       #### Not used in this problem. 
        'TIMES',        # *
        'TRUE',         # true
        'VAR',          # var
)

states = (
    ('javascriptcomment', 'exclusive'),
)

t_ANDAND = r'&&'
t_COMMA = r","
t_DIVIDE = r"/"
t_ELSE = r"else"
t_EQUALEQUAL = r"=="
t_EQUAL = r"="
t_FALSE = r"false"
t_FUNCTION = r"function"
t_GE = r">="
t_GT = r">"
t_IF = r"if"
t_LBRACE = r"{"
t_LE = r"<="
t_LPAREN = r"\("
t_LT = r"<"
t_MINUS = r"-"
t_NOT = r"!"
t_OROR = r"\|\|"
t_PLUS = r"\+"
t_RBRACE = r"}"
t_RETURN = r"return"
t_RPAREN = r"\)"
t_SEMICOLON = r";"
t_TIMES = r"\*"
t_TRUE = r"true"
t_VAR = r"var"


def t_javascriptcomment(token):
    r'/\*'
    token.lexer.begin('javascriptcomment')

def t_javascriptcomment_end(token):
    r'\*/'
    token.lexer.lineno += token.value.count('\n')
    token.lexer.begin('INITIAL')

def t_javascriptcomment_error(token):
    token.lexer.skip(1)
    
def t_eolcomment(token):
    r'//[^\n]*'
    pass

t_ignore = ' \t\v\r' # whitespace 

def t_STRING(token):
    r'"[^"]*(?:\"[^"]*)*"'
    token.value = token.value[1:-1]
    return token
#
def t_IDENTIFIER(token):
    r'[a-zA-Z][a-zA-Z_]*'
    return token

def t_NUMBER(token):
    r'-?[0-9]+\.?[0-9]*'
    token.value = float(token.value)
    return token

def t_newline(t):
        r'\n'
        t.lexer.lineno += 1

def t_error(t):
        print "JavaScript Lexer: Illegal character " + t.value[0]
        t.lexer.skip(1)

# We have included two test cases to help you debug your lexer. You will
# probably want to write some of your own. 

lexer = lex.lex() 

def test_lexer(input_string):
  lexer.input(input_string)
  result = [ ] 
  while True:
    tok = lexer.token()
    if not tok: break
    result = result + [tok.type]
  return result

input1 = """ - !  && () * , / ; { || } + < <= = == > >= else false function
if return true var """

output1 = ['MINUS', 'NOT', 'ANDAND', 'LPAREN', 'RPAREN', 'TIMES', 'COMMA',
'DIVIDE', 'SEMICOLON', 'LBRACE', 'OROR', 'RBRACE', 'PLUS', 'LT', 'LE',
'EQUAL', 'EQUALEQUAL', 'GT', 'GE', 'ELSE', 'FALSE', 'FUNCTION', 'IF',
'RETURN', 'TRUE', 'VAR']

print test_lexer(input1)
print test_lexer(input1) == output1

input2 = """
if // else mystery  
=/*=*/= 
true /* false 
*/ return"""

output2 = ['IF', 'EQUAL', 'EQUAL', 'TRUE', 'RETURN']

print test_lexer(input2)
print test_lexer(input2) == output2
