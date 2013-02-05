grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    start = tuple(init)
    is_goal = lambda x: x == tuple(goal)
    p = shortest_path_search(start, rmsuccessors, is_goal)
    if p == 'fail':
        return p
    else:
        return [(len(p)-1)/2]+goal
    # you should RETURN your result

def rmsuccessors(s):
    q = {}
    for x in delta:
        nx = [x[i]+s[i] for i in range(len(x))]
        nx = tuple(nx)
        if nx[0] >= 0 and nx[1] >= 0 and nx[0] < len(grid) and nx[1] < len(grid[0]):
            if grid[nx[0]][nx[1]] == 0:
                q[nx] = x
    return q
            
Fail = "fail"

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
