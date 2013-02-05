import random

def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def do(action, state):
    "Apply action to state, returning a new state."
    (score, yard, cards) = state
    next_card = random.choice(cards)
    if action == 'gather':
        return (score+yard, 0, cards[1:]) if next_card == 'F' else (score+yard, 0, cards[:-1]) 
    if action == 'wait':
        if next_card == 'F':
            return (score, 0, cards[1:])
        elif next_card == 'H':
            return (score, yard+1, cards[:-1])
        raise ValueError
    
def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)

def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    print average_score(A), average_score(B) 
    return average_score(A) - average_score(B) > 1.5

def strategy(state):
    (score, yard, cards) = state
    if 'F' in cards:
        if yard < cards.count('H')/ (cards.count('F')+1):
            return 'wait'
        else:
            return 'gather'
    else:
        return 'wait'

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or 
            gather == (9, 0, 'F'*4 + 'H'*9))
    
    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))
    
    assert superior(strategy)
    return 'tests pass'

print test()   
