from copy import deepcopy
from math import log
from random import randrange

nums = open("dijkstraData.txt")
graph = {}
line = nums.readline()
while line:
    nodes = line.split()
    graph[int(nodes[0])] = {}
    for i in nodes[1:]:
        #print i, i.split(',')
        p, q = i.split(',')
        graph[int(nodes[0])][int(p)] = int(q)
    line = nums.readline()
print len(graph)

g = [7,37,59,82,99,115,133,165,188,197]

def search(goal):
    start = 1
    action_cost = lambda x: x
    is_goal = lambda x: x==goal
    p = lowest_cost_search(start, opsuccessors, is_goal, action_cost)
    return path_cost(p)
    # you should RETURN your result

def opsuccessors(s):
    return graph[s]
            
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
    
for k in g:
    print search(k)
    
            
    
