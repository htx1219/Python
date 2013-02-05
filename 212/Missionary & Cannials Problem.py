def mc_problem(start=(3,3,1,0,0,0), goal=None):
    """Solve the missionaries and cannibals problem.
    State in 6 ints:(M1, C1, B1, M2, C2, B2) on the start (1) and other(2) sides
    Find a path that goes from the initial state to the goal state (which, if
    not specified, is the state with no people or boats on the starts side."""
    M1, C1, B1, M2, C2, B2 = start
    if goal == None:
        goal = (0,0,0,M1, C1, B1)
    if start == goal:
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        for (state, action) in csuccessors(path[-1]).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)
                
    return Fail
            
Fail = []
    

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    if C1 > M1 > 0 or C2 > M2 > 0 or M1<0 or M2<0 or C1<0 or C2<0:
        return {}
    items = []
    if B1 > 0:
        items += [(sub(state,delta), a + '->') for delta, a in deltas.items()]
    if B2 > 0:
        items += [(add(state,delta), '<-' + a) for delta, a in deltas.items()]
    return dict(items)

deltas = {(2,0,1,-2,0,-1):'MM',
          (0,2,1,0,-2,-1):'CC',
          (1,1,1,-1,-1,-1):'MC',
          (1,0,1,-1,0,-1):'M',
          (0,1,1,0,-1,-1):'C'}

def add(X, Y):
    "Add two vectors, X and Y."
    return tuple(x+y for x,y in zip(X,Y))

def sub(X, Y):
    "subtract two vectors, X and Y."
    return tuple(x-y for x,y in zip(X,Y))

print mc_problem()
