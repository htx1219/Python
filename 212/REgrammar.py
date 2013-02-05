from functools import update_wrapper
import re

def grammar1(description):
    """Convert a description to a grammar"""
    G = {}
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ',1)
        alternatives = split(rhs, '|  ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def grammar(description, whitespace='\s*'):
    """Convert a description to a grammar.  Each line is a rule for a
    non-terminal symbol; it looks like this:
        Symbol =>  A1 A2 ... | B1 B2 ... | C1 C2 ...
    where the right-hand side is one or more alternatives, separated by
    the '|' sign.  Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.
    
    Notation for *, +, or ? not allowed in a rule alternative (but ok
    within a token). Use '\' to continue long lines.  You must include spaces
    or tabs around '=>' and '|'. That's within the grammar description itself.
    The grammar that gets defined allows whitespace between tokens by default;
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between tokens)."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ')
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ',1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit= -1):
    "Like str.split applied to text, but strips white space from each piece"
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

G = grammar(r"""
Exp      => Term [+-] Exp | Term
Term     => Factor [*/] Term | Factor
Factor   => Funcall | Var | Num | [(] Exp [)]
Funcall  => Var [(] Exp [)]
Exps     => Exp [,] Exp | Exp
Var      => [a-zA-Z]\w*
Num      => [-+]?[0-9]+([.][0-9]*)?
""")

#G = {'Exp': (['Tern', '[+-]', 'Exp'],[
#    'Term']), 'Term':(....)...)


def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        #print 'now parse sequence'
        for atom in sequence:
            #print 'seq: ',atom, sequence
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
            #print 'result: ',result, "text: ",text, "tree ", tree
        return result, text

    @memo
    def parse_atom(atom, text):
        #print 'now parse atom'
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                #print 'atom: ',alternative, atom
                tree, rem = parse_sequence(alternative, text)
                #print 'non terminal?', atom, 'tree: ', tree, 'rem: ',rem
                if rem is not None: return [atom]+tree, rem  
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            #if m:
                #print 'now else', tokenizer, m, (m.group(1), text[m.end():])
            return Fail if (not m) else (m.group(1), text[m.end():])
    
    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)

# The following decorators may help you solve this question. HINT HINT!

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

@decorator
def n_ary(f):
    def n_ary_f(x,*args):
        return x if not args else f(x, n_ary_f(*args))
    update_wrapper(n_ary_f, f)
    return n_ary_f

def verify(G):
    lhstokens = set(G) - set([' '])
    rhstokens = set(t for alts in G.values() for alt in alts for t in alt)
    def show(title, tokens): print title,'=',' '.join(sorted(tokens))
    show('Non-terms', G)
    show('Terminals', rhstokens-lhstokens)
    show('Suspects ', [t for t in (rhstokens - lhstokens) if t.isalnum()])
    show('Orphans  ', lhstokens - rhstokens)

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:
            return m
        
def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]

def lit(x): return lambda t: set([t[len(x):]]) if t.startswith(x) else null
@n_ary
def seq(x,y): return lambda t: set().union(*map(y, x(t)))
def alt(x,y): return lambda t: x(t)|y(t)
def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null
dot = lambda t: set([t[1:]]) if t else null
eol = lambda t: set(['']) if t == '' else null
def star(x): return lambda t:(set([t]) |
                              set(t2 for t1 in x(t) if t1 != t
                                  for t2 in star(x)(t1)))
def plus(x): return lambda t: star(x)(t[(len(t)-len(x(t).pop())):]) if x(t) != null else null
def opt(x): return lambda t: x(t)|set([t])

null = frozenset()

REGRAMMAR = grammar("""
RE      => seq | star | plus | opt | alt | parren | lit
seq     => element seq | element
element => star | plus | opt | alt | parren | lit
plus    => single [+]
star    => single [*]
single  => alt | opt | parren | lit
lit     => [^()?|+*]
parren  => [(] RE [)]
alt     => lit [|] lit
opt     => parren [?] | lit [?]
""", whitespace='')

def parse_re(pattern):
    #print parse('RE', pattern, REGRAMMAR)[0]
    return convert(parse('RE', pattern, REGRAMMAR)[0])


@memo
def convert(tree, dic=REGRAMMAR):
    if tree[0] in REGRAMMAR.keys():
        sec = tree
    elif tree[0][0] in REGRAMMAR.keys():
        sec = tree[0]
    #print sec
    if sec[0] == 'RE':
        return convert(sec[1])
    elif sec[0] =='seq':
        try:
            return seq(convert(sec[1]), convert(sec[2]))
        except IndexError:
            return convert(sec[1])
    elif sec[0] =='element':
        return convert(sec[1])
    elif sec[0] =='plus':
        return plus(convert(sec[1]))
    elif sec[0] =='star':
        return star(convert(sec[1]))
    elif sec[0] =='single':
        return convert(sec[1])
    elif sec[0] =='lit':
        return lit(sec[1])
    elif sec[0] =='parren':
        return convert(sec[2])
    elif sec[0] =='alt':
        return alt(convert(sec[1]), convert(sec[3]))
    elif sec[0] =='opt':
        return opt(convert(sec[1]))
    #print tree
    return tree

def test_re_grammar():
    pattern = "(ab*)?c+"
    parse('RE', pattern, REGRAMMAR)

#t = parse('RE', "d(ab*)?c+", REGRAMMAR)

print parse_re("(abd?)+")('ababdabcdddef')
