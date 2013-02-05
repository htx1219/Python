N = 8

def possible(state, car, N=N):
    q = state[search_tuple(state, car)][1]
    d = q[1]-q[0]
    assert d==1 or d==N
    poss = ()
    while True:
        if search_place(state, q[-1]+(len(poss)+1)*d) and search_place(state, q[-1]+(len(poss)+1)*d) !='@':
            break
        else:
            poss = poss+(d*(len(poss)+1),)
    forward = len(poss)
    while True:
        if search_place(state, q[0]-(len(poss)-forward+1)*d) and search_place(state, q[0]-(len(poss)-forward+1)*d) !='@' :
            break
        else:
            poss = (-d*(len(poss)-forward+1),)+poss
    return poss

def new_state(state, car, p):
    assert search_tuple(state, car)
    i = search_tuple(state, car)
    new_place = tuple([s+p for s in state[i][1]])
    new_state = state[:i]+((car, new_place),)+state[i+1:]
    return new_state

def search_tuple(x, q):
    for i, n in enumerate(x):
        if n[0] == q:
            return i
    return None

def search_place(x, n):
    for i, m in enumerate(x):
        if n in m[1]:
            return m[0]
    return None


def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    def parkingsuccessors(state, N=N):
        result = []
        for car in [i[0] for i in state if i[0] != '@' and i[0] !='|']:
            poss = possible(state, car, N)
            result += [(new_state(state, car, p) ,(car, p)) for p in poss]
        return dict(result)
    def is_goal(state):
        for car in state[search_tuple(state, '*')][1]:
            if car in state[search_tuple(state, '@')][1]:
                return True
        return False
    return shortest_path_search(start, parkingsuccessors, is_goal)


# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    q = (start,)
    while n > 1:
        q = q+(q[-1]+incr,)
        n -= 1
    return q


def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    if N%2 ==0:
        goal = N*N/2 -1
    else:
        goal = N*(N/2+1)-1
    wall = ()
    for i in range(N*N):
        if i in range(N) or i in range(N*(N-1), N*N) or i%N == 0 or (i-7)%N ==0:
            if i != goal:
                wall = wall+(i,)
    return (('@', (goal,)),)+cars+(('|', wall),)


def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))


puzzle4 = grid((
    ('*', locs(29, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
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
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]



##puzzle1 = (
## ('@', (31,)),
## ('*', (26, 27)), 
## ('G', (9, 10)),
## ('Y', (14, 22, 30)), 
## ('P', (17, 25, 33)), 
## ('O', (41, 49)), 
## ('B', (20, 28, 36)), 
## ('A', (45, 46)), 
## ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
##        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))
