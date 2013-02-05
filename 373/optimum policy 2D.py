grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 2] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------

is_goal = lambda x: (x[0],x[1]) == tuple(goal)
action_cost = lambda x: cost[x+1]

def search():
    start = tuple(init)
    p = lowest_cost_search(start, opsuccessors, is_goal, action_cost)
    return p
    # you should RETURN your result

def opsuccessors(s):
    q = {}
    for x in action:
        new_o = (s[2]+x) % len(forward)
        k = forward[new_o]
        nx = (s[0]+k[0], s[1]+k[1], new_o)
        if nx[0] >= 0 and nx[1] >= 0 and nx[0] < len(grid) and nx[1] < len(grid[0]):
            if grid[nx[0]][nx[1]] == 0:
                q[nx] = x
    return q
            
Fail = "fail"

def lowest_cost_search(start, successors, is_goal, action_cost):
    """Return the lowest cost path, starting from start state,
    and considering successors(state) => {state:action,...},
    that ends in a state for which is_goal(state) is true,
    where the cost of a path is the sum of action costs,
    which are given by action_cost(action)."""
    explored = set()
    frontier = [ [start] ]
    if is_goal(start):
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        state1 = final_state(path)
        if is_goal(state1):
            return path
        explored.add(state1)
        pcost = path_cost(path)
        for (state, action) in successors(state1).items():
            if state not in explored:
                total_cost = pcost +action_cost(action)
                path2 = path + [(action, total_cost), state]
                frontier.append(path2)
                add_to_frontier(frontier, path2)
    return Fail

def path_cost(path):
    "The total cost of a path (which is stored in a tuple with the final action)."
    if len(path) < 3:
        return 0
    else:
        action, total_cost = path[-2]
        return total_cost

def add_to_frontier(frontier, path):
    "Add path to frontier, replacing costlier path if there is one."
    # (This could be done more efficiently.)
    # Find if there is an old path to the final state of this path.
    old = None
    for i,p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return # Old path was better; do nothing
    elif old is not None:
        del frontier[old] # Old path was worse; delete it
    ## Now add the new path and re-sort
    frontier.append(path)
    frontier.sort(key=path_cost)

def final_state(path): return path[-1]

def optimum_policy2D():
    path = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    p = search()
    for i in range(0, len(p)-1, 2):
        path[p[i][0]][p[i][1]] = action_name[p[i+1][0]+1]
    path[p[-1][0]][p[-1][1]] = "*"
    return path

policy = optimum_policy2D()
for i in policy:
    print i
