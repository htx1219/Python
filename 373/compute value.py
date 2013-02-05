grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def compute_value():
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    step = 0
    frontier = [goal]
    while frontier:
        k = frontier.pop(0)
        if k == goal and closed[k[0]][k[1]] == 0:
            value[k[0]][k[1]] = 0
            closed[k[0]][k[1]] = 1
        else:
            left = value[k[0]][k[1]-1] if k[1]-1 >=0 else 99
            right = value[k[0]][k[1]+1] if k[1]+1 <len(grid[0]) else 99
            top = value[k[0]-1][k[1]] if k[0]-1 >=0 else 99
            below = value[k[0]+1][k[1]] if k[0]+1 <len(grid) else 99
            value[k[0]][k[1]] = min(left, right, top, below) + cost_step
        for i in range(len(delta)):
            x2 = k[0] + delta[i][0]
            y2 = k[1] + delta[i][1]
            if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                if grid[x2][y2] == 0 and closed[x2][y2] == 0:
                    frontier.append([x2, y2])
                    closed[x2][y2] = 1
    return value #make sure your function returns a grid of values as demonstrated in the previous video.

value = compute_value()
for i in value:
    print i
