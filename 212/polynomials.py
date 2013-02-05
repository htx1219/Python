from functools import update_wrapper

def decorator(d):
    def _d(fn):
        return update_wrapper(d(fn),fn)
    update_wrapper(_d,d)
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
            #some element of args can't be a dict key
            return f(args)
    return _f

def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""
    coefs = tuple(coefs)
    return poly_memo(coefs)

@memo
def poly_memo(coefs):
    q = ''
    for i, n in enumerate(coefs):
        i_s, n_s = str(i), str(n)
        if (not n==1) and (not n==0):
            q = q+' + '+n_s
        if i == 0:
            if n==1:
                q = q+ ' + 1'
        elif i==1:
            if n==1:
                q = q+' + x'
            elif n != 0:
                q = q+' * x'
        else:
            if n ==1:
                q = q +' + x**'+i_s
            elif n !=0:
                q = q + ' * x**'+i_s
    b = (q[2:]+' ').split('+')
    b.reverse()
    ans = '+'.join(b)
    #print b, ans, q
    ans = ans[1:-1]
    p = lambda x:eval(ans)
    p.__name__ = ans
    p.coefs = coefs
    return p


"""
simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
"""

def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    try:
        if isinstance(x.coefs, tuple):
            for i in x.coefs:
                if not isinstance(i, int):
                    return False
            return True
    except:
        pass
    return False

def pad(x, n):
    while len(x) < n:
        x = x+(0,)
    return x
               
def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    coef = ()
    p1_c, p2_c = p1.coefs, p2.coefs
    if len(p1_c)< len(p2_c):
        p = pad(p1_c, len(p2_c))
        for x in range(len(p2_c)):
            coef = coef+(p[x]+p2_c[x],)
    else:
        p = pad(p2_c, len(p1_c))
        for x in range(len(p1_c)):
            coef = coef+(p[x]+p1_c[x],)
    return poly(coef)
    

def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    coef = ()
    p1_c, p2_c = p1.coefs, p2.coefs
    if len(p1_c)< len(p2_c):
        p = pad(p1_c, len(p2_c))
        for x in range(len(p2_c)):
            coef = coef+(p[x]-p2_c[x],)
    else:
        p = pad(p2_c, len(p1_c))
        for x in range(len(p1_c)):
            coef = coef+(p1_c[x]-p[x],)
    return poly(coef)


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    p1_c, p2_c = p1.coefs, p2.coefs
    coef = [0]*(len(p1_c)+len(p2_c)-1)
    for i, n in enumerate(p1_c):
        for j, m in enumerate(p2_c):
            coef[i+j] += m*n
    return poly(tuple(coef))
    


def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    ans = p
    while n > 1:
       ans = mul(ans, p)
       n -= 1
    return ans

def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    p_c = p.coefs
    ans = [0]*(len(p_c)-1)
    for i in range(len(p_c)-1):
        ans[i] = p_c[i+1]*(i+1)
    return poly(ans)


def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    p_c = p.coefs
    ans = [0]*(len(p_c)+1)
    for i in range(len(p_c)):
        ans[i+1] = p_c[i]/(i+1)
    ans[0] = C
    return poly(ans)


def test_poly():
    global p1, p2, p3, p4, p5, p9 # global to ease debugging in an interactive session

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x**2 + 20 * x + 10
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    assert p9 == poly([0,0,0,0,0,0,0,0,0,1])
    assert p9(2) == 512
    p4 =  add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert (power(poly((1, 1)), 10).__name__ == 
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

    assert add(poly((10, 20, 30)), poly((1, 2, 3))) == poly((11, 22, 33))
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))) == poly((9, 18, 27))
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))) == poly((10, 40, 100, 120, 90))
    assert power(poly((1, 1)), 2) == poly((1, 2, 1))
    assert power(poly((1, 1)), 10) == poly((1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1))

    assert deriv(p1) == poly((20, 60))
    assert integral(poly((20, 60))) == poly((0, 20, 30))
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573
    print 'tests pass'


def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""
    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
    return canonical_name(name1) == canonical_name(name2)

    
test_poly()


"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the 
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""


def test_poly1():
    # I define x as the polynomial 1*x + 0.
    x = poly((0, 1))
    # From here on I can create polynomials by + and * operations on x.
    newp1 =  30 * x**2 + 20 * x + 10 # This is a poly object, not a number!
    assert p1(100) == newp1(100) # The new poly objects are still callable.
    assert p1.__name__ == newp1.__name__
    assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 1))
    print 'test1 pass'

def test_poly2():
    newp1 = Poly('30 * x**2 + 20 * x + 10')
    assert p1(100) == newp1(100)
    assert p1.__name__ == newp1.__name__
    assert Poly('x + 1') * Poly('x - 1') == Poly('x**2 - 1')
    print 'test2 pass'

test_poly1()
test_poly2()
