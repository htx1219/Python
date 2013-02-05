from __future__ import division
import itertools
import time
import string, re
import cProfile       
                
def cryp():
    odds = range(100, 1000)
    evens = range(1000, 10000)
    return next((odd,odd*2)
                for odd in odds
                if str(odd)[1] == str(odd)[2]
                if odd*2 in evens
                if str(odd*2)[0] == str(odd*2)[2]
                if len(set([str(odd)[0],str(odd)[1], str(odd*2)[0],str(odd*2)[1],
                           str(odd*2)[3]])) == len([str(odd)[0],str(odd)[1], str(odd*2)[0],str(odd*2)[1],
                           str(odd*2)[3]]))
#print cryp()
#print timedcalls(1.0, cryp)
#cProfile.run('cryp()')

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return f       
    
def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(set(re.findall(r'[A-Z]',formula)))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)

def valid(f):
    "Formula f is valid if it has no numbers with leading zero, and evals true"
    try:
        return not re.search(r'\b0[0-9]',f) and eval(f) is True
    except ArithmeticError:
        return False

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if word.isupper():
        """
        result = [(str(10**(len(word)-i-1))+'*'+word[i]) for i
                  in range(len(word))]"""
        result = [('%s*%s' % (10**i, d)) for (i, d) in enumerate(word[::-1])]
        return '('+'+'.join(result)+')'
    else:
        return word

def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. The first digit of a multi-digit 
    number can't be 0. So if YOU is a word in the formula, and the function
    is called with Y eqal to 0, the function should return False."""    
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    parms = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    first_letters = ''.join(set(re.findall(r'\b[A-Z]', formula)))
    zero = "*".join(first_letters)
    f2 = '('+zero+" != 0)"
    f = 'lambda %s: %s*%s' % (parms, body, f2) 
    if verbose: print f
    return eval(f), letters

def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass

def test():
    assert faster_solve('A + B == BA') == None # should NOT return '1 + 0 == 01'
    assert faster_solve('YOU == ME**2') == ('289 == 17**2' or '576 == 24**2' or '841 == 29**2')
    assert faster_solve('X / X == X') == '1 / 1 == 1'
    return 'tests pass'

cProfile.run('faster_solve("ODD + ODD == EVEN")')



