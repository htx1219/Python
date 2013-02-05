def more_pour_problem(capacity, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    def mpsuccessors(state):
        result = []
        result += [(state[:x]+(0,)+state[x+1:], ('empty', x)) for x in range(len(capacity))]
        result += [(state[:x]+(capacity[x],)+state[x+1:], ('fill', x)) for x in range(len(capacity))]
        result += [(state[:x]+(0,)+state[x+1:y]+(state[x]+state[y],)+state[y+1:]
                    if state[x]+state[y]<capacity[y]
                    else state[:x]+(state[x]+state[y]-capacity[y],)+state[x+1:y]+(capacity[y],)+state[y+1:],
                    ('pour', x,y)) for x in range(len(capacity)) for y in range(x+1,len(capacity))]
        result += [(state[:x]+(state[x]+state[y],)+state[x+1:y]+(0,)+state[y+1:]
                    if state[x]+state[y]<capacity[x]
                    else state[:x]+(capacity[x],)+state[x+1:y]+(state[x]+state[y]-capacity[x],)+state[y+1:],
                    ('pour', y,x)) for x in range(len(capacity)) for y in range(x+1,len(capacity))]
        return dict(result)
    if start == None:
        start = (0,)*len(capacity)
    is_goal = lambda x: goal in x
    return shortest_path_search(start, mpsuccessors, is_goal)
    
def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []
    
def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()
