#We will consider the following regular expressions:
#
#       single characters       #       a       
#       regexp1 regexp2         #       ab
#       regexp *                #       a*
#       regexp1 | regexp2       #       a|b
#       ( regexp )              #       (a|b)* -- same as (?:a|b) 
#
# That's it. We won't consider [a-c] because it's just a|b|c, and we won't
# consider a+ because it's just aa*. We will not worry about escape
# sequences. Single character can be a-z, A-Z or 0-9 -- that's it. No need
# to worry about strange character encodings. We'll use ( ) for regular
# expression grouping instead of (?: ) just to make the problem simpler.
#
# Don't worry about precedence or associativity. We'll fully parenthesize
# all regular expressions before giving them to you. 
#
# You will write a procedure re_to_nfsm(re_string). It takes as input a
# single argument -- a string representing a regular expression. It returns
# a tuple (edges,accepting,start) corresponding to an NSFM that accepts the
# same language as that regular expression.
#
# Hint: Make a lexer and a paser and an interpreter. Your interpreter may
# find it handy to know the current state and the goal state. Make up as
# many new states as you need. 

import ply.lex as lex
import ply.yacc as yacc


tokens = (
        'SINGLE',
        'LPAREN',
        'RPAREN',
        'STAR',
        'OR',
        )

t_SINGLE = r'[a-zA-Z0-9]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_STAR = r'\*'
t_OR = r'\|'

t_ignore = ' \t\v\r'

def t_error(t):
    print "RE Lexer: Illegal character " + t.value[0]
    t.lexer.skip(1)

start = 'RE'

def p_elt_or(p):
    'elt : elt OR elt'
    p[0] = ('or', p[1], p[3])

def p_RE_elts(p):
    'RE : elts'
    p[0] = ('re', p[1])

def p_elts(p):
    'elts : elt elts'
    p[0] = [p[1]] + p[2]

def p_elts_empty(p):
    'elts : '
    p[0] = []

def p_elt_single(p):
    'elt : SINGLE'
    p[0] = ('single', p[1])

def p_elt_star(p):
    'elt : elt STAR'
    p[0] = ('star', p[1])

def p_elt_paren(p):
    'elt : LPAREN RE RPAREN'
    p[0] = p[2]

def p_error(p):
    print "RE parserL Illegal grammar!"

# Fill in your code here. 

def interpret(ast):
    result = []
    global nfsm
    nfsm = 1
    if ast[0] == 're':
        eval_re(ast[1], result)
    else:
        print 'Wrong input type: ', ast[0]
    return put_dict(result), [len(ast[1])+1], 1

def eval_re(ast, result):
    global nfsm
    m = nfsm
    nfsm += len(ast)+1
    for i, n in enumerate(ast):
        eval_elt(n, result, m+i, m+i+1)

def eval_elt(elt, result, start, goal):
    global nfsm
    n = nfsm
    #print "start and goal", start, goal
    e_type = elt[0]
    if e_type == 'single':
        result.append(((start, elt[1]), [goal]))
    elif e_type == 'star':
        result.append(((start, None), [goal]))
        eval_elt(elt[1], result, goal, goal)
    elif e_type == 'or':
        eval_elt(elt[1], result, start, goal)
        eval_elt(elt[2], result, start, goal)
    elif e_type == 're':
        result.append(((start, None), [n]))
        eval_re(elt[1], result)
        result.append((((n+len(elt[1]), None)), [goal]))

def put_dict(result):
    d = {}
    for i in result:
        try:
            if i[1][0] not in d[i[0]]:
                d[i[0]] += i[1]
        except:
            d[i[0]] = i[1]
    return d	

lexer = lex.lex() 
parser = yacc.yacc() 

def get_tree(re_string): 
    # Feel free to overwrite this with your own code.
    lexer.input(re_string)
    parse_tree = parser.parse(re_string, lexer=lexer) 
    return parse_tree

def re_to_nfsm(re_string): 
    # Feel free to overwrite this with your own code.
    lexer.input(re_string)
    parse_tree = parser.parse(re_string, lexer=lexer)
    return interpret(parse_tree) 

# We have included some testing code ... but you really owe it to yourself
# to do some more testing here.

def nfsmaccepts_buggy(edges,accepting,current,string,visited):
    visited = [(current,string)] + visited
    if (current,None) in edges: # epsilon transitions
        for dest in edges[(current,None)]:
            if nfsmaccepts(edges,accepting,dest,string,visited):
                return True
    if string == "":
        return current in accepting
    elif (current,string) in visited:
        return False
    letter = string[0]
    rest = string[1:]
    if (current,letter) in edges:
        for dest in edges[(current,letter)]:
            if nfsmaccepts(edges,accepting,dest,rest,visited):
                return True
    return False

def nfsmaccepts(edges, accepting, current, string, visited): 
    """Check if a given string is accepted by a non-deterministic finite state
    machine, returning True if so, and False if not."""
    # Do not continue if we have been to this state before
    #print "current: ", current
    if (current, string) in visited:
        return False
    visited.append((current, string))
    # Check possible epsilon transitions
    if (current, None) in edges:
        for dest in edges[(current, None)]:
            if nfsmaccepts(edges, accepting, dest, string, visited):
                return True
    # If the input is empty and no epsilon transitions lead to 
    # accepting state, check if the current state is accepting
    if string == '':
        return current in accepting
    # Check normal letter transitions
    letter = string[0]
    rest = string[1:]
    if (current, letter) in edges:
        for dest in edges[(current, letter)]:
            #print dest
            if nfsmaccepts(edges, accepting, dest, rest, visited):
                return True
    return False

def test(re_string, e, ac_s, st_s, strings):
    #print get_tree(re_string)
    my_e, my_ac_s, my_st_s = re_to_nfsm(re_string)
    print my_e#, my_ac_s, my_st_s
    for string in strings:
        print nfsmaccepts(e,ac_s,st_s,string,[])==nfsmaccepts(my_e,my_ac_s,my_st_s,string,[]) 

def re_t(string):
    my_e, my_ac_s, my_st_s = re_to_nfsm(string)
    return lambda x: nfsmaccepts(my_e,my_ac_s,my_st_s,x,[]) 

edges = { (1,'a')  : [ 2 ] ,
          (2,None) : [ 3 ] ,    # epsilon transition
          (2,'b')  : [ 2 ] ,
          (3,'c')  : [ 4 ] } 
accepting_state = [4]
start_state = 1

test("a(b*)c", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 

edges = {(3, 'c'): [4],
         (2, None): [5],
         (6, None): [3],
         (5, None): [6],
         (1, 'a'): [2],
         (5, 'b'): [5]}

edges = { (1,'a')  : [ 2 ] ,
          (2,'b') :  [ 1 ] ,    
          (1,'c')  : [ 3 ] ,
          (3,'d')  : [ 1 ] } 
accepting_state = [1]
start_state = 1

test("((ab)|(cd))*", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  )

# a
edges = { (1, 'a') : [2] }
accepting_states = [2]
start_state = 1
test ('a', edges, accepting_states, start_state,
      ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb'])

# ab
edges = { (1, 'a') : [2],
          (2, 'b') : [3] }
accepting_states = [3]
start_state = 1
test ('ab', edges, accepting_states, start_state,
      ['', 'a', 'b', 'ab', 'ba', 'aa', 'bb'])

# a*
edges = { (1, 'a') : [1] }
accepting_states = [1]
start_state = 1
test('a*', edges, accepting_states, start_state,
     ["", "a", "aa", "aaa", "b", "aab", "baa"])

# a|b
edges = { (1, 'a') : [2],
          (1, 'b') : [2] }
accepting_states = [2]
start_state = 1
test('a|b', edges, accepting_states, start_state,
     ["", "a", "aa", "aaa", "b", "aab", "baa"])
