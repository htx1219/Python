import random

def shuffle(deck):
    N = len(deck)
    swapped = [False]*N
    while not all(swapped):
        i,j = random.randrange(N), random.randrange(N)
        swapped[i] = swapped[j] = True
        swap(deck,i,j)

def swap(deck,i,j):
    deck[i], deck[j] = deck[j], deck[i]

if __name__ == '__main__':
    initial_deck = ['a','b','c']
    N = len(initial_deck)
    TRIES = 10000
    deck_permutations = {}

    deck = initial_deck[:]
    for t in range(TRIES):
        shuffle(deck)
        deck_str = str(deck)

        if deck_str not in deck_permutations:
            deck_permutations[deck_str] = 1
        else:
            deck_permutations[deck_str] += 1

        #reset deck    
        deck = initial_deck[:]

    for j in deck_permutations:
        print j, '=>', deck_permutations[j]*1.0/TRIES
