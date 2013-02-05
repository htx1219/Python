from nose.tools import eq_
from REinterp import re_to_nfsm, nfsmaccepts

def ensure(regex, string, correct=True):
    edges, accepting, starting = re_to_nfsm(regex)
    assert correct == nfsmaccepts(edges, accepting, starting, string, []), ( "Error: {} \n {} \n {} \n {}".format(edges, accepting, starting, string))
    print "Congratulations! you pass the test!"

def given_1_test():
    for i in range(10):
        ensure("a(b*)c", 'a' + 'b'*i + 'c')

def given_2_test():
    for s in [ "", "ab", "cd", "abcd", "cdcd", "abcdab" ]:
        ensure("((ab)|(cd))*", s)

def tok_test():
    ensure("a", "a")
    ensure('a', 'b', False)

def two_tok_test():
    ensure("ab", "ab")
    ensure("ab", "ba", False)
    ensure("ab", "b", False)
    ensure("ab", "a", False)

def choice_test():
    ensure("a|b", "a")
    ensure("a|b", "b")
    ensure("a|b", "ab", False)

def star_test():
    for i in range(10):
        ensure("a*", "a"*i)

def paren_test():
    ensure("(a)", "a")
    ensure("(a)", "b", False)
    ensure("(a)", "aa", False)

def paren_star_test():
    for i in range(10):
        ensure("(a)*", "a"*i)

def paren_bar_test():
    ensure("(ab)|(bc)", "ab")
    ensure("(ab)|(bc)", "bc")
    ensure("(ab)|(bc)", "abc", False)

def empty_test():
    ensure("", "")
    ensure("", "a", False)

def branch_star_test():
    ensure("a|(b*)", "a")
    for i in range(10):
        ensure("a|(b*)", "b"*i)
    ensure("a|(b*)", 'ba', False)
    ensure("a|(b*)", 'ab', False)

def star_branch_test():
    ensure("a*|b", "b")
    for i in range(10):
        ensure("a*|b", "a"*i)
    ensure("a*|b", 'ba', False)
    ensure("a*|b", 'ab', False)
