def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1 

def inverse(f, delta = 1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = delta
        while f(x) < y:
            x = x*2
            # Now x is too big, x-delta is too small; pick the closest to y
        l = x/2
        r = x
        return bin_search(l, r, f, y, delta)
    return f_1

def bin_search(l, r, f, y, delta):
    m = (l+r)/2
    if f(m) >= y and f(m-delta) <= y:
        return m if (f(m)-y < y-f(m-delta)) else m-delta
    if f(m) < y:
        return bin_search(m, r, f, y, delta)
    else:
        return bin_search(l, m, f, y, delta)    
   
def square(x): return x*x
sqrt = slow_inverse(square)

print sqrt(1000000000)

sqrt1 = inverse(square)
print sqrt1(1000000000)
