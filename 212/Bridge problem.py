import doctest

def bsuccessors3(state):
    """Return a dict of {state:action} pairs.  State is (here, there, light)
    where here and there are frozen sets of people, light is 0 if the light is 
    on the here side and 1 if it is on the there side.
    Action is a tuple (travelers, arrow) where arrow is '->' or '<-'"""
    here, there, light = state
    if light == 0:
        return dict(((here  - frozenset([a,b]),
                      there | frozenset([a, b]), 1),
                     (set([a, b]), '->'))
                    for a in here for b in here)
    else:
        return dict(((here  | frozenset([a,b]),
                      there - frozenset([a, b]),0),
                     (set([a, b]), '<-'))
                    for a in there for b in there) 

def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [ [(here, frozenset(),0)] ]
    if not here or here == frozenset(['light']):
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        here, there, t = path[-1]
        if not here or here == frozenset(['light']):
            return path
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                here, there, t = state
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time)
    return []

def elapsed_time(path):
    return path[-1][2]

def bridge_problem2(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [ [(here, frozenset())] ]
    if not here or here == frozenset(['light']):
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        here, there = state1 = final_state(path)
        if not here or here == frozenset(['light']):
            return path
        explored.add(state1)
        pcost = path_cost(path)
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                total_cost = pcost+bcost(action)
                path2 = path + [(action, total_cost), state]
                frontier.append(path2)
                add_to_frontier(frontier, path2)
    return []

def final_state(path): return path[-1]

def add_to_frontier(frontier, path):
    "Add path to frontier, replacing costiler path if there is one."
    # (This could be done more efficiently.)
    # Find if there is an old path to the final state of this path
    old = None
    for i, p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return
    elif old is not None:
        del frontier[old]
    frontier.append(path)

def bsuccessors2(state):
    """Return a dict of {state:action} pairs. A state is a
    (here, there) tuple, where here and there are frozensets
    of people (indicated by their travel times) and/or the light."""
    here, there = state
    if 'light' in here:
        return dict(((here  - frozenset([a,b, 'light']),
                      there | frozenset([a, b, 'light'])),
                     (a, b, '->'))
                    for a in here if a is not 'light'
                    for b in here if b is not 'light')
    else:
        return dict(((here  | frozenset([a,b, 'light']),
                      there - frozenset([a, b, 'light'])),
                     (a, b, '<-'))
                    for a in there if a is not 'light'
                    for b in there if b is not 'light') 

def path_cost(path):
    """The total cost of a path (which is stored in a tuple
    with the final action."""
    # path = [state, (action, total_cost), state, ... ]
    if len(path) < 3:
        return 0
    else:
        return path[-2][1]
        
def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are 
    # times; arrow is a string. 
    a, b, arrow = action
    return max(a,b)

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
    '<-' for there to here."""
    here, there, t = state
    if 'light' in here:
        result = {}
        q = [(x, y) for x in here for y in here if x!='light' and y != 'light']
        for i in q:
            result[(here-frozenset([i[0], i[1], 'light']),
                    there|frozenset([i[0],i[1], 'light']),t+max(i))]= (i[0], i[1], '->')
        return result
    elif 'light' in there:
        result = {}
        q = [(x, y) for x in there for y in there if x!='light' and y != 'light']
        for i in q:
            result[(here|frozenset([i[0], i[1], 'light']),
                    there-frozenset([i[0],i[1], 'light']),t+max(i))] = (i[0], i[1], '<-')
        return result

# seems we should seperate the light into antoher term in state, and make it
# (here, there, t, light)

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test():

    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
                (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) =={
                (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    
    return 'tests pass'

#print test()
print bridge_problem((1,2,5,10))[1::2]

class TestBridge: """
>>> elapsed_time(bridge_problem([1,2,5,10]))
17

## There are two equally good solutions
>>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

"""

print doctest.testmod()
