test1 = [ ("var","x"),                  # var x 
          ("var","y"),                  # var y 
          ("var","z"),                  # var z 
          ("add",["x","y","z"]),        # x = y + z
          ("set",["y","z"]),            # y = z 
          ("add",["z","x","x"]), ]      # z = x + x

def interesting1(test):
    # The test is interesting if it contains "A + B" on some line
    # and "var A" and "var B" _before_ that line. Let's hack something
    # up that simulates that.
    for i in range(len(test)):
        line = test[i]
        if line[0] == "add":
            if line[1] == [x for x in line[1] if ("var",x) in test[:i]]:
                return True 
    return False

import itertools
itern = 0


def autodebug_fail(test, interesting, result = None): 
    # find the smallest subset of test that is still interesting!
    q = test[:]
    if not interesting(test):
        return None
    if result == None:
        result = []
    for i in range(len(test)):
        global itern
        itern += 1
        if itern % 100000 == 0:
            print 'iter times, ', itern, result
        q.remove(q[i])
        if interesting(q):
            result.append(q)
            autodebug(q, interesting, result)
            #result = [min(result, key=len)]
            #print result
        q = test[:]
    return min(result, key=len)

def autodebug(test, interesting): 
    # find the smallest subset of test that is still interesting!
    q = test[:]
##    q.reverse()
##    print q, test
    result = []
    l = len(test)
    poss = itertools.product('10', repeat=l)
    for i in poss:
        global itern
        itern += 1
        if itern % 100000 == 0:
            print 'iter times, ', itern, result
        new_q = [q[n] for n, j in enumerate(i) if j == '1']
        if interesting(new_q):
            result.append(new_q)
            #result = [min(result, key = len)]
    if not interesting(test):
        return None
    return min(result, key=len)

print autodebug(test1, interesting1) == \
      [('var', 'x'),
       ('var', 'z'),
       ('add', ['z', 'x', 'x'])]

def interesting2(lst):
    # For this one, a list is interesting if it contains three numbers
    # in strict ascending order.
    for i in range(len(lst)):
        for j in range(i):
            for k in range(j):
                if lst[k] < lst[j] and lst[j] < lst[i]:
                    return True
    return False

# Random numbers
test2 = [ 2270, 10193, 10149, 32125, 18656, 2275, 1548, 3418, 13155, 25667, 9520, 4896, 10667 ]  

ans = autodebug(test2, interesting2)
print ans
print len(ans) == 3
print interesting2(ans) 
