"""
high play-pig fu(A,B) ->A winner
stratagy f(state)->hold or roll
mid: state(p, me, you, pending)
actions roll(state)->set of {state}; hold(state)->state
roll(state, die)->state
low:die-int
score-int goal-int, to move-0 or 1 players-by stategy
"""
import random
import collections
from functools import update_wrapper
import itertools
import time

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    _f.cache = cache
    return _f

##State = namedtuple('state', 'p me you pending')
##s = State(1,2,3,4)
##
##def hold_1(state):
##    return State(other[state.p], state.you, state.me + state.pending, 0)
##
##def roll_1(state, d):
##    if d == 1:
##        return State(other[state.p], state.you, state.me+1, 0)
##    else:
##        return State(state.p, state.me, state.you, state.pending+d)

def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (p, me, you, pending) = state
    if d == 1:
        return (other[p], you, me+1, 0) # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)

other = {0:1, 1:0}

possible_moves = ['roll', 'hold']

def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)

def hold_at(x):
    """Return a strategy that holds if and only if 
    pending >= x or player reaches goal."""
    def strategy(state):
        (p, me, you, pending) = state
        return 'hold' if pending >= x or pending + me >= goal else 'roll'
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy

goal = 40

def play_pig(A, B, dierolls=dierolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategies = [A, B]
    state = (0, 0, 0, 0)
    while True:
        (p, me, you, pending) = state
        if me >= goal:
            return strategies[p]
        elif you >= goal:
            return strategies[other[p]]
        elif strategies[p](state) == 'hold':
            state = hold(state)
        elif strategies[p](state) == 'roll':
            state = roll(state, next(dierolls))
        else:
            return strategies[other[p]]
    
def always_roll(state):
    return 'roll'

def always_hold(state):
    return 'hold'

def illegal_strategy(state):
    return 'I want to win pig please'

def Q_pig(state, action, Pwin):  
    "The expected value of choosing action in state."
    if action == 'hold':
        return 1 - Pwin(hold(state))
    if action == 'roll':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError

def pig_actions(state):
    "The legal actions form a state."
    _, _, _, pending = state
    return ['roll','hold'] if pending else ['roll']

def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U"
    def EU(action): return Q(state, action, U)
    return max(actions(state), key = EU)

@memo
def Pwin(state):
    """The utility of a tate; here just the probablity that an optimal player
    whose turn it is to move can win from the current state"""
    # Assume opponent also plays with optimal strategy.
    (p, me, you, pending) = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig(state, action, Pwin) for action in pig_actions(state))

@memo
def win_diff(state):
    (p, me, you, pending) = state
    if me + pending >= goal or you >= goal:
        return (me + pending - you)
    else:
        return max(Q_pig(state, action, win_diff)
                   for action in pig_actions(state))

def max_wins(state):
    "The optimal pig strategy chooses an action with the highest win probability."
    return best_action(state, pig_actions, Q_pig, Pwin)

def max_diffs(state):
    """A strategy that maximizes the expected difference between my final score
    and my opponent's"""
    return best_action(state, pig_actions, Q_pig, win_diff)

def test():
    assert(max_diffs((1, 26, 21, 15))) == "hold"
    assert(max_diffs((1, 23, 36, 7)))  == "roll"
    assert(max_diffs((0, 29, 4, 3)))   == "roll"
    # The remaining test cases are examples where max_wins and
    # max_diffs return different actions.
    assert(max_diffs((0, 36, 32, 5)))  == "roll"
    assert(max_diffs((1, 37, 16, 3)))  == "roll"
    assert(max_diffs((1, 33, 39, 7)))  == "roll"
    assert(max_diffs((0, 7, 9, 18)))   == "hold"
    assert(max_diffs((1, 0, 35, 35)))  == "hold"
    assert(max_diffs((0, 36, 7, 4)))   == "roll"
    assert(max_diffs((1, 5, 12, 21)))  == "hold"
    assert(max_diffs((0, 3, 13, 27)))  == "hold"
    assert(max_diffs((0, 0, 39, 37)))  == "hold"
    assert(max_wins((1, 5, 34, 4)))   == "roll"
    assert(max_wins((1, 18, 27, 8)))  == "roll"
    assert(max_wins((0, 23, 8, 8)))   == "roll"
    assert(max_wins((0, 31, 22, 9)))  == "hold"
    assert(max_wins((1, 11, 13, 21))) == "roll"
    assert(max_wins((1, 33, 16, 6)))  == "roll"
    assert(max_wins((1, 12, 17, 27))) == "roll"
    assert(max_wins((1, 9, 32, 5)))   == "roll"
    assert(max_wins((0, 28, 27, 5)))  == "roll"
    assert(max_wins((1, 7, 26, 34)))  == "hold"
    assert(max_wins((1, 20, 29, 17))) == "roll"
    assert(max_wins((0, 34, 23, 7)))  == "hold"
    assert(max_wins((0, 30, 23, 11))) == "hold"
    assert(max_wins((0, 22, 36, 6)))  == "roll"
    assert(max_wins((0, 21, 38, 12))) == "roll"
    assert(max_wins((0, 1, 13, 21)))  == "roll"
    assert(max_wins((0, 11, 25, 14))) == "roll"
    assert(max_wins((0, 22, 4, 7)))   == "roll"
    assert(max_wins((1, 28, 3, 2)))   == "roll"
    assert(max_wins((0, 11, 0, 24)))  == "roll"
    return 'tests pass'

#print test()

strategies = [clueless, hold_at(goal/4), hold_at(goal/3), hold_at(goal/2), hold_at(goal), max_wins, max_diffs]

def play_tournament(strategies, series_length = 50):
    result = collections.defaultdict(int)
    for A, B in itertools.combinations(strategies, 2):
        for _ in range(series_length):
            if play_pig(A, B) == A:
                result[A, B] += 1
            else:
                result[B, A] += 1
            if play_pig(B, A) == A:
                result[A, B] += 1
            else:
                result[B, A] += 1
    result = dict(result)
    print (report_tournament(strategies, result))

def report_tournament(strategies, result):
    N = len(strategies)
    table = []
    for s in strategies:
        items = [result.get((s, t), 0) for t in strategies]
        items = ['{0:<15}'.format(s.__name__)]+map('{0:>5}'.format, items + [sum(items)])
        print(' '.join(items))

play_tournament(strategies)

def compare_strategies(A, B):
    states = [(0, me, you, pending)
             for me in range(goal+1) for you in range(goal+1) for pending in range(goal+1)
             if me + pending <= goal]
    #print len(states)
    r = collections.defaultdict(int)
    for s in states: r[A(s), B(s)] += 1
    print dict(r)

#compare_strategies(max_wins, max_diffs)

def story():
    r = collections.defaultdict(lambda: [0,0])
    states = [(0, me, you, pending)
             for me in range(goal+1) for you in range(goal+1) for pending in range(goal+1)
             if me + pending <= goal]
    for s in states:
        w, d = max_wins(s), max_diffs(s)
        if w != d:
            _, _, _, pending = s
            i = 0 if (w == 'roll') else 1
            r[pending][i] += 1
    for (delta, (wrolls, drolls)) in sorted(r.items()):
        print '%4d: %3d %3d' % (delta, wrolls, drolls)

#story()

def timedcall(fn, *args):
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

print timedcall(Pwin, (0,0,0,0))
print len(Pwin.cache)

def Pwin2(state):
   """The utility of a state; here just the probability that an optimal player
   whose turn it is to move can win from the current state."""
   _, me, you, pending = state
   return Pwin3(me, you, pending)

@memo
def Pwin3(me, you, pending):
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        state = (0, me, you, pending)
        return max(Q_pig(state, action, Pwin2) for action in pig_actions(state))
   
def test():
    epsilon = 0.00000001 # used to make sure that floating point errors don't cause test() to fail
    assert goal == 40
    assert len(Pwin3.cache) <= 50000
    assert Pwin2((0, 42, 25, 0)) == 1
    assert Pwin2((1, 12, 43, 0)) == 0
    assert Pwin2((0, 34, 42, 1)) == 0
    assert abs(Pwin2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
    assert abs(Pwin2((0, 19, 35, 4)) - 0.493173612834) <= epsilon
    #print len(Pwin3.cache) 
    return 'tests pass'

print test()

