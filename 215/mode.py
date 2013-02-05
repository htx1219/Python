from operator import itemgetter

def mode2(L):
    d = {}
    for i in L:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    max = 0
    mode = None
    for k, v in d.iteritems():
        if v > max:
            max = v
            mode = k
    return mode

    m = L[0]
    for k in d:
        if d[k]> d[m]:
            m = k
    return m

def mode(L):
    k = max(L)
    t = [0 for i in range(k+1)]
    for i in L:
        #print t, k, i
        t[i] += 1
    m = L[0]
    w = 0
    for i in range(k+1):
        if t[i] > w:
            m = i
            w = t[i]
    return m

####
# Test
#
import time
from random import randint

def test():
    assert 5 == mode([1, 5, 2, 5, 3, 5])
    iterations = (10, 20, 30, 100, 200, 300, 1000, 5000, 10000, 20000, 30000)
    times = []
    for i in iterations:
        L = []
        for j in range(i):
            L.append(randint(1, 10))
        start = time.clock()
        for j in range(500):
            mode(L)
        end = time.clock()
        print start, end
        times.append(float(end - start))
    slopes = []
    for (x1, x2), (y1, y2) in zip(zip(iterations[:-1], iterations[1:]), zip(times[:-1], times[1:])):
        print (x1, x2), (y1, y2)
        slopes.append((y2 - y1) / (x2 - x1))
    # if mode runs in linear time, 
    # these factors should be close (kind of)
    print slopes

test()
