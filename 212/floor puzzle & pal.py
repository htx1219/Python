import itertools

def floor_puzzle():
    "return a tuple(WATER, ZEBRA) indicating their house numbers."
    floors = bottom,_,_,_,top = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(floors))
    return [[Hopper, Kay, Liskov, Perlis, Ritchie] for Hopper, Kay, Liskov, Perlis, Ritchie in orderings
                if Hopper != top
                if Kay != bottom
                if Liskov != top and Liskov != bottom
                if Perlis > Kay
                if abs(Ritchie-Liskov) != 1
                if abs(Liskov-Kay) != 1][0]

print floor_puzzle()

def floor_puzzle2():
    "return a tuple(WATER, ZEBRA) indicating their house numbers."
    floors = bottom,_,_,_,top = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(floors))
    for Hopper, Kay, Liskov, Perlis, Ritchie in orderings:
        if Hopper != top and Kay != bottom and Liskov != top and Liskov != bottom:
            if Perlis > Kay and abs(Ritchie-Liskov) != 1 and abs(Liskov-Kay) != 1:
                return [Hopper, Kay, Liskov, Perlis, Ritchie]

def longest_subpalindrome_slice(sentence):
    start, end = 0, 0
    check_pal.times = 0
    if len(sentence)>=1:
        start, end = 0, 1
    for i in range(len(sentence)-1):
        if check_pal(sentence[i:i+2]):
            start_new, end_new = opal(sentence, i, i+2)
            if end_new - start_new > end - start:
                start, end = start_new, end_new
    for i in range(len(sentence)-2):
        if check_pal(sentence[i:i+3]):
            start_new, end_new = opal(sentence, i, i+3)
            if end_new - start_new > end - start:
                start, end = start_new, end_new
    print check_pal.times
    return (start, end)

def check_pal(word):
    pal = True
    check_pal.times += 1
    for i in range(int(len(word)/2)):
        pal = pal and word[i].upper() == word[-i-1].upper()
    return pal

def opal(sentence, start, end):
    if check_pal(sentence[start-1:end+1]) and start-1 >= 0 and end+1 <= len(sentence):
        return opal(sentence, start-1, end+1)
    else:
        return start, end

def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    assert L('x') == (0, 1)
    return 'tests pass'

print test()
