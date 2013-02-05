ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return False
invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

# check_sudoku should return True
hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]

from copy import deepcopy

def check_row_form(l):
    if len(l) != 9:
        return False
    nonz = [i for i in l if i != 0]
    allnum = set(range(1,10))
    if not set(nonz) <= allnum:
        return False
    return True
    
def check_row(l):
    nonz = [i for i in l if i != 0]
    if len(nonz) != len(set(nonz)):
        return False
    return True

def check_sudoku(grid):
    if len(grid) != 9:
        return None
    for i in grid:
        k = check_row_form(i)
        if not k:
            return None
    for i in grid:
        k = check_row(i)
        if not k:
            return False
    for i in range(9):
        l = [j[i] for j in grid]
        k = check_row(l)
        if not k:
            return False
    for i in range(9):
        j = grid[3*(i/3):3*(i/3+1)]
        l = [r[3*(i%3): 3*(i%3 + 1)] for r in j]
        m = l[0] + l[1] + l[2]
        k = check_row(m)
        if not k:
            return False
    return True

def give_part(i, j, grid):
    p = 3*(i/3)+(j/3)
    k = grid[3*(p/3):3*(p/3+1)]
    l = [r[3*(p%3): 3*(p%3 + 1)] for r in k]
    m = l[0] + l[1] + l[2]
    return (grid[i], [k[j] for k in grid], m)

def give_xy(i, j):
    res = [0,0,0]
    res[0] = [(i, k) for k in range(9)]
    res[1] = [(k, j) for k in range(9)]
    p = 3*(i/3)+(j/3)
    res[2] = [(m, n) for m in range(3*(p/3), 3*(p/3)+3) for n in range(3*(p%3), 3*(p%3)+3)]
    return res

def make_pos(grid):
    pos = deepcopy(grid)
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                a, b, c = give_part(i, j, grid)
                p = set(range(1,10))
                p = p-set(a) -set(b) - set(c)
                pos[i][j] = p
    return pos

def update_pos(pos, i, j, n):
    pos[i][j] = n
    parts = give_xy(i, j)
    #print i, j, n
    #if i == 0 and j == 5:
#        print pos
    #for w in pos:
        #print w
    for m in parts:
        for k in m:
            if type(pos[k[0]][k[1]]) == set:
                pos[k[0]][k[1]] = pos[k[0]][k[1]] - set([n])
    return pos

def single_choice(pos):
    change = True
    while change:
        change = False
        for i in range(9):
            for j in range(9):
                target = pos[i][j]
                if type(target) == set:
                    res = only_pos(i, j, pos)
                    change = change or res
                tarhet = pos[i][j]
                if type(target) == set:
                    if len(target) == 1:
                        update_pos(pos,i,j, target.pop())
                        change = True
    return pos

def only_pos(i, j, pos):
    change = False
    parts = give_xy(i, j)
    for elt in pos[i][j]:
        for part in parts:
            count = 0
            for k in range(9):
                target = pos[part[k][0]][part[k][1]] 
                if type(target) == set:
                    if elt in target:
                        count += 1
            if count == 1:
                update_pos(pos, i, j, elt)
                change = True
                return True
    return change
        
    

def not_pos(pos):
    for i in range(9):
        for j in range(9):
            target = pos[i][j]
            if type(target) == set:
                if len(target) == 0:
                    return True
    return False

def finished(pos):
    for i in range(9):
        for j in range(9):
            target = pos[i][j]
            if type(target) == set:
                return False
    return True

def choose_one(posi):
    posj = deepcopy(posi)
    for i in range(9):
        for j in range(9):
            if type(posj[i][j]) == set:
                for elt in posj[i][j]:
                    pos = deepcopy(posj)
                    pos = update_pos(pos, i, j, elt)
                    #print i, j, pos[i][j]
                    pos = single_choice(pos)
                    if not not_pos(pos):
                        if finished(pos):
                            return pos
                        posn = choose_one(pos)
                        if posn:
                            return posn
                return None
    return None

def solve_sudoku(grid):
    if not check_sudoku(grid):
        return check_sudoku(grid)
    k = make_pos(grid)
    if finished(k):
        return k
    m = single_choice(k)
    if not_pos(m):
        return False
    k = deepcopy(m)
    k = choose_one(k)
    #for i in k:
        #print i
    if not_pos(k):
        return False
    if check_sudoku(k):
        return k
    else:
        return False
        

print check_sudoku(ill_formed) # --> None
print check_sudoku(valid)      # --> True
print check_sudoku(invalid)    # --> False
print check_sudoku(easy)       # --> True
print check_sudoku(hard)       # --> True
