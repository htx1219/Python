import itertools

import random

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
mydeck_with_poker = [r+s for r in '23456789TJQKA' for s in 'SHDC']+['?B']+['?R']
wild_B = [r+s for r in '23456789TJQKA' for s in 'SC']
wild_R = [r+s for r in '23456789TJQKA' for s in 'HD']

def deal (numhands, n=5, deck=mydeck):
    "Return a list of hands from the deck"
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]

def deal_poker (numhands, deck=mydeck):
    "Return a list of hands from the deck"
    random.shuffle(deck)
    hands = []
    common_hand = deck[0:5]
    for i in range(numhands):
        hands.append(common_hand+[deck[5+i*2]]+[deck[5+i*2+1]])
    return hands

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    hands = set(best_hand(h) for h
                in itertools.product(*map(replacements, hand)))
    return max(hands, key=hand_rank1)

def replacements(card):
    if card == '?B': return wild_B
    elif card == '?R': return wild_R
    else: return [card]

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    return max(itertools.combinations(hand,5), key= hand_rank1)
"""
def all_hands(hand):
    total_hands = []
    for i in range(len(hand)-1, 0, -1):
        for j in range(i-1, -1, -1):
            new_hand = []
            comb = range(0,len(hand))
            comb.remove(i)
            comb.remove(j)
            for k in comb:
                new_hand.append(hand[k])
            total_hands.append(new_hand)
    return total_hands

def wild_hands(hand):
    "Return all best hands for ?B and ?R replaced by all possible cards"
    wild_B = [r+s for r in '23456789TJQKA' for s in 'SC']
    wild_R = [r+s for r in '23456789TJQKA' for s in 'HD']
    winning_hand = []
    if hand_contain(hand, '?B'):
        for cb in wild_B:
            using_hand = hand[:]
            using_hand.remove('?B')
            using_hand.append(cb)
            winning_hand.append(wild_hands(using_hand))
    if hand_contain(hand, '?R'):
        for cr in wild_R:
            using_hand = hand[:]
            using_hand.remove('?R')
            using_hand.append(cr)
            winning_hand.append(wild_hands(using_hand))
    if hand_contain(hand, '?R') == False and hand_contain(hand,'?B')==False:
        winning_hand = [best_hand(hand)]
    return poker(winning_hand)
    
def hand_contain(hand, key):
    for i in hand:
        if i == key:
            return True
    return False
"""
def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand, ...]"
    return max(hands, key=hand_rank1)

def hand_rank1(hand):
    "Return a value indicating how high the hand ranks"
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4 , 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return (9 if (5,) == counts else
            8 if straight and flush else
            7 if (4, 1) == counts else
            6 if (3, 2) == counts else
            5 if flush else
            4 if straight else
            3 if (3, 1, 1) == counts else
            2 if (2, 2, 1) == counts else
            1 if (2, 1, 1, 1) == counts else
            0), ranks

def group(items):
    "Return a list of [(count, x)...] highest count first, then highest x first"
    groups = [(items.count(x), x ) for x in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs):
    return zip(*pairs)

def test_best_hand():
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C','8C','9C','TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C','8S','TC','TD','TH'])
    assert (sorted(best_hand("TD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D','7H','7S','TD'])
    return 'test_best_hand passes'

print test_best_hand()
hand="6C 7C 8C 9C TC 5C JS".split()

def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'

print test_best_wild_hand()
hand="6C 7C 8C 9C TC ?B ?R".split()

hand_names = ["5 of a kind","Straight Flush", "4 of a Kind", "Full House", "Flush", "Straight", "3 of a Kind", "Two Pairs", "Pair", "High Cards"]
hand_names.reverse()

def hand_percentages(n=700*1000, deck= mydeck):
    "Sample n random hands and print a table of percentages for each type of hand"
    counts = [0]*10
    for i in range(n/10):
        for hand in deal_poker(10, deck=deck):
            ranking = hand_rank1(wild_hands(hand))[0]
            counts[ranking] +=1
        if i%50 == 0:
            print str(i*7)+' hands checked!'
    for i in reversed(range(10)):
        print "%14s: %6.3f %%" % (hand_names[i], 100.*counts[i]/n)

#hand_percentages(70000)

