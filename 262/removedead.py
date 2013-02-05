def removedead(fragment,returned):
    f_r = fragment[::-1]
    live_v = returned[:]
    LIVE = []
    for stmt in f_r:
        print 'Live vars are ', live_v
        if stmt[0] in live_v:
            LIVE.append(stmt)
            live_v += stmt[1]
            live_v.remove(stmt[0])
    return LIVE[::-1]
        

# We have provided a few test cases. You may want to write your own.

fragment1 = [ ("a", ["1"]), 
              ("b", ["2"]), 
              ("c", ["3"]), 
              ("d", ["4"]), 
              ("a", ["5"]), 
              ("d", ["c","b"]), ]

fragment2 = [ ("a", ["1"] ) ,           # a = 1
              ("b", ["a", "1"] ),       # b = a operation 1
              ("c", ["2"] ), ]   

print removedead(fragment1, ["a","d"]) == \
        [('b', ['2']), 
         ('c', ['3']), 
         ('a', ['5']), 
         ('d', ['c', 'b'])]

print removedead(fragment2, ["c"]) == [('c', ['2'])]

print removedead(fragment1, ["a"]) == [('a', ['5'])]

print removedead(fragment1, ["d"]) == \
        [('b', ['2']), 
         ('c', ['3']), 
         ('d', ['c', 'b'])]
