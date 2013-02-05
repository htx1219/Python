##def double_out_search(total):
##    """Return a shortest possible list of targets that add to total,
##    where the length <= 3 and the final element is a double.
##    If there is no solution, return None."""
##    def dartsuccessors(state):
##        result = []
##        all_dart = all_darts()
##        for dart in all_dart:
##            result += [(state+(dart,), dart)]
##        #print result
##        return dict(result)
##    start = ()
##
##    ans = shortest_path_search(start, dartsuccessors, is_goal)
##    if ans == []:
##        return None
##    else:
##        path = ans[1::2]
##        return path
##
##def is_goal(state):
##    if sum([dart_score(i) for i in state])==total:
##        if state[-1][0] == 'D':
##            return True
##    return False
##
##
##
##def shortest_path_search(start, successors, is_goal):
##    """Find the shortest path from start state to a state
##    such that is_goal(state) is true."""
##    if is_goal(start):
##        return [start]
##    explored = set() # set of states we have visited
##    frontier = [ [start] ] # ordered list of paths we have blazed
##    while frontier:
##        path = frontier.pop(0)
##        s = path[-1]
##        for (state, action) in successors(s).items():
##            if state not in explored:
##                explored.add(state)
##                path2 = path + [action, state]
##                if is_goal(state):
##                    return path2
##                else:
##                    frontier.append(path2)
##    return []

def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    result = []
    score = set(range(1,21)+[2*i for i in range(1, 21)]+[3*i for i in range(1, 21)])
    score = score|set((25, 50))
    score = list(score)
    score.sort(reverse = True)
    score = [0]+score
    #print score
    res = []
    for i in score:
        for j in score:
            for k in score:
                if (k%2 == 0 and k<= 40 and k!=0) and i+j+k == total:
                    if i != 0: res = res + [name(i)[0]]
                    if j != 0: res = res + [name(j)[0]]
                    return res+['D'+str(k/2)]
                elif k==50 and i+j+k == total:
                    if i != 0: res = res + [name(i)[0]]
                    if j != 0: res = res + [name(j)[0]]
                    return res+['DB']
    return None

def name(d):
    res = []
    if d<=20:
        res += ['S'+str(d)]
    if d<=40 and d%2 == 0:
        res += ['D'+str(d/2)]
    if d<=60 and d%3 == 0:
        res += ['T'+str(d/3)]
    if d == 50: res += ['DB']
    if d == 25: res += ['SB']
    return res


def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
    print 'tests pass'

#test_darts()

clock = '20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5'.split()

def other_section(q):
    i = clock.index(q)
    new_clock = [clock[-1]]+clock+[clock[0]]
    return (new_clock[i], new_clock[i+2])

def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    poss = []
    if target == 'SB':
        prob = miss
        poss = [('S'+str(i), prob/20) for i in range(1, 21)]
        poss += [('DB', miss*miss), ('SB', (1-miss)-miss*miss)]
    elif target == 'DB':
        prob = miss*2
        poss = [('S'+str(i), prob/20) for i in range(1, 21)]
        poss += [('SB', miss), ('DB', 1-3*miss)]
    elif target[0] == 'S':
        prob = miss/5
        poss = [('S'+target[1:], 1-prob), ('D'+target[1:], prob/2), ('T'+target[1:], prob/2)]
        n = target[1:]
        poss = [((x[0]+other_section(n)[0], p*prob/2),
                 (x[0]+other_section(n)[1], p*prob/2),
                 (x[0]+n, p*(1-prob))) for x, p in poss]
        poss = poss[0]+poss[1]+poss[2]
    elif target[0] == 'D':
        prob = miss
        poss = [('D'+target[1:], 1-prob), ('S'+target[1:], prob/2), ('OFF', prob/2)]
        n = target[1:]
        poss = [((x[0]+other_section(n)[0], p*prob/2),
                 (x[0]+other_section(n)[1], p*prob/2),
                 (x[0]+n, p*(1-prob))) for x, p in poss if x != 'OFF']
        poss = poss[0]+poss[1]+(('OFF', prob/2),)
    elif target[0] == 'T':
        prob = miss
        poss = [('T'+target[1:], 1-prob), ('S'+target[1:], prob)]
        n = target[1:]
        poss = [((x[0]+other_section(n)[0], p*prob/2),
                 (x[0]+other_section(n)[1], p*prob/2),
                 (x[0]+n, p*(1-prob))) for x, p in poss]
        poss = poss[0]+poss[1]
    poss_non_zero = [(x, p) for x, p in poss if p != 0.0]
    return dict(poss_non_zero)

OFF = 0

def dart_score(dart):
    ans = 1
    mult = {'S':1, 'D':2, 'T':3}
    if dart[1] == 'B':
        return mult[dart[0]]*25
    if dart == 'OFF':
        return OFF
    else:
        return mult[dart[0]]*int(dart[1:])

def all_darts():
    ans = []
    mult_re = {1:'S', 2:'D', 3:'T'}
    for i in range(21):
        for j in range(3):
            if i == 0:
                if j != 2:
                    ans.append(mult_re[j+1]+'B')
            else:
                ans.append(mult_re[j+1]+str(i))
    return ans

def best_target(miss):
    "Return the target that maximizes the expected score."
    darts = all_darts()
    res = []
    for dart in darts:
        if dart != 'SB' and dart != 'DB':
            q = outcome(dart, miss).items()
            e_score = sum([dart_score(x)*p for x, p in q])
            res.append((e_score,dart))
    res.sort()
    return res[-1][1]
    
def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert same_outcome(
        outcome('SB', 0.2),
        {'S9': 0.01, 'S8': 0.01, 'S3': 0.01, 'S2': 0.01, 'S1': 0.01, 'DB': 0.04,
         'S6': 0.01, 'S5': 0.01, 'S4': 0.01, 'S19': 0.01, 'S18': 0.01, 'S13': 0.01,
         'S12': 0.01, 'S11': 0.01, 'S10': 0.01, 'S17': 0.01, 'S16': 0.01,
         'S15': 0.01, 'S14': 0.01, 'S7': 0.01, 'S20': 0.01, 'SB': 0.76})
    print 'test2 pass'

test_darts2()
