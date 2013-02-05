import time

def timedcall(fn, *args):
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

# WORDS = set(file('words4k.txt').read().upper().split())

def prefixes(word):
    "A list of the inital sequences of a word, not including the complete word"
    return [word[:i] for i in range(len(word))]

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def readwordlist(filename):
    """Read the words from a file and return a set of the words 
    and a set of the prefixes."""
    file = open(filename) # opens file
    text = file.read()    # gets file into string
    wordset = set(text.upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

def find_words_nested(letters):
    results = set()

    def extend_prefix(w, letters):
        if w in WORDS: results.add8(w)
        if w not in PREFIXES: return
        for L in letters:
            extend_prefix(w+L, removed(letters,L))

    extend_prefix('', letters)
    return results

def find_words(letters, pre='', result = None):
    if results is None: result = set()
    if pre in WORDS: result.add(pre)
    if pre in PREFIXES:
        for L in letters:
            find_words(letters.replace(L, '', 1), pre+L, results)
    return results

def word_plays(hand, board_letters):
    "Find all word plays from hand that can be made to abut with a letter on board."
    # Find prefix + L + suffix; L from board_letters, rest from hand
    results = set()
    for pre in find_prefixes(hand, '', set()):
        for L in board_letters:
            add_suffixes(removed(hand, pre), pre+L, results)
    return results

cache_prefixes = {}

def find_prefixes_simple_and_naive(hand, pre='', results=None):
    "Find all prefixes (of words) that can be made from letters in hand."
    if pre == '':
        try:
            return cache_prefixes[hand]
        except:
            pass
    if results is None: results = set()
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)
    if pre == '':
        cache_prefixes[hand] = results 
    return results

def add_suffixes_simple_and_naive(hand, pre, results):
    """Return the set of words that can be formed by extending pre with letters in hand."""
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in hand:
            add_suffixes(hand.replace(L, '', 1), pre+L, results)
    return results

def longest_words(hand, board_letters):
    "Return all word plays, longest first."
    words = word_plays(hand, board_letters)
    return sort(words, key=len, reverse = True)

POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)

def word_score(word):
    "The sum of the individual letter point scores for this word."
    return sum(POINTS[L] for L in word)

def topn(hand, board_letters, n=10):
    "Return a list of the top n words that hand can play, sorted by word score."
    words = word_plays(hand, board_letters)
    return sorted(words, reverse = True, key = word_score)[:n]

class anchor(set):
    "An anchor is where a new word can be placed; has a set of allowable letters"

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

ANY = anchor(LETTERS)

mnx, moab = anchor('MNX'), anchor('MOAB')
a_row = row = ['|', 'A', mnx, moab, '.', '.', ANY, 'B', 'E', ANY, 'C', ANY,
               '.', ANY, 'D', ANY, '|']
a_hand = 'ABCEHKN'

# if isinstance(row[i], anchor)

def row_plays(hand, row):
    "Return a set of legal plays in row. A row play is an (i, 'WORD') pair."
    results = set()
    ## To each alloable prefix, add all suffixes, keeping words
    for (i, sq) in enumerate(row[1:-1], 1):
        if isinstance(sq, anchor):
            pre, maxsize = legal_prefix(i, row)
            if pre: ## Add to the letters already on the borad
                start  = i - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored = False)
            else: ## Empty to left: go through the set of all possible prefixes
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row,
                                     results, anchored = False)
    return results
        
def legal_prefix(i, row):
    """A legal prefix of an anchor at row[i] is either a string of letters
    already on the board, or new letters that fit into an empty space.
    Return the tuple (prefix_on_board, maxsize) to indicate this.
    E.g. legal_prefix(a_row, 9) == ('BE', 2) and for 6, ('',2)"""
    s = i
    while is_letter(row[s-1]): s -= 1
    if s < i:
        return ''.join(row[s:i]), i-s
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor): s -= 1
    return ('', i-s)

def is_empty(sq):
    'Is this an empty square(no letters, but a valid position on board)'
    return sq == '.' or sq == '*' or isinstance(sq, anchor)

def is_letter(sq):
    return isinstance(sq, str) and sq in LETTERS

def add_suffixes(hand, pre, start, row, results, anchored=True):
    "Add all possible suffixes, and accumulate (start, word) pairs in results."
    i = start + len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]):
        results.add((start, pre))
    if pre in PREFIXES:       
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre+sq, start, row, results)        
        elif is_empty(sq):        
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(hand.replace(L, '', 1), pre+L, start, row, results)
    return results

prev_hand, prev_results = '', set()

def find_prefixes(hand, pre = '', results = None):
    ## Cache the most recent full hand (don't cache intermediate results)
    global prev_hand, prev_results
    if hand == prev_hand: return prev_results
    if results is None: results = set()
    if pre == '': prev_hand, prev_results = hand, results
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)
    return results

def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

def show_simple_and_naive(board):
    "Print the board."
    for x in board:
        print ' '.join(x)
    return None

def find_cross_word(board, i, j):
    """Find the vertical word that crosses board[j][i]. Return (j2, w),
    where j2 is the starting row, and w is the word"""
    sq = board[j][i]
    w = sq if is_letter(sq) else '.'
    for j2 in range(j, 0, -1):
        sq2 = board[j2-1][i]
        if is_letter(sq2): w = sq2 + w
        else: break
    for j3 in range(j+1, len(board)):
        sq3 = board[j3][i]
        if is_letter(sq3): w = w + sq3
        else: break
    return (j2, w)

def neighbors(board, i, j):
    """Return a list of the contents of the four neighboring squares,
    in the order N,S,E,W."""
    return [board[j-1][i], board[j+1][i],
            board[j][i+1], board[j][i-1]]

def set_anchors(row, j, board):
    """Anchors are empty squares with a neighboring letter. Some are resticted
    by cross-words to be only a subset of letters."""
    for (i, sq) in enumerate(row[1:-1], 1):
        neighborlist = (N,S,E,W) = neighbors(board, i, j)
        # Anchors are squares adjacent to a letter.  Plus the '*' square.
        if sq == '*' or (is_empty(sq) and any(map(is_letter, neighborlist))):    
            if is_letter(N) or is_letter(S):   
                # Find letters that fit with the cross (vertical) word
                (j2, w) = find_cross_word(board, i, j)
                row[i] = anchor(L for L in LETTERS if w.replace('.', L) in WORDS)
            else: # Unrestricted empty square -- any letter will fit.
                row[i] = ANY

def horizontal_plays(hand, board):
    "Return a set of legal plays in row. A row play is an (i, 'WORD') pair."
    results = set()
    ## To each alloable prefix, add all suffixes, keeping words
    for (j, row) in enumerate(board[1:-1], 1):
        set_anchors(row, j, board)
        #col = [x[j] for x in board]
        for (i, word) in row_plays(hand, row):
            score = calculate_score(board, (i,j), ACROSS, hand, word)
            results.add((score, (i,j), word))
    return results

def transpose(matrix):
    "Transpose e.g. [[1,2,3], [4,5,6]] to [[1, 4], [2, 5], [3, 6]]"
    # or [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    return map(list, zip(*matrix))

def all_plays(hand, board):
    """All plays in both directions. A play is a (pos, fir, word) tuple,
    where pos is an (i, j) pair, and dir is ACROSS or DOWN."""
    hplays = horizontal_plays(hand, board)
    vplays = horizontal_plays(hand, transpose(board))
    return (set((score, (i, j), ACROSS, w) for (score, (i,j), w) in hplays) |
            set((score, (i, j), DOWN, w) for (score, (j,i), w) in vplays))

ACROSS, DOWN = (1, 0), (0, 1)

def calculate_score(board, pos, direction, hand, word):
    "Return the total score for this play"
    total, crosstotal, word_mult = 0,0,1
    starti, startj = pos
    di, dj = direction
    other_direction = DOWN if direction == ACROSS else ACROSS
    for (n, L) in enumerate(word):
        letter_mult = 1
        i, j = starti + n*di, startj + n*dj
        sq = board[j][i]
        b = BONUS[j][i]
        word_mult *= (1 if is_letter(sq) else
                      3 if b == TW else 2 if b in (DW, '*') else 1)
        letter_mult *= (1 if is_letter(sq) else
                      3 if b == TL else 2 if b == DL else 1)
        total += POINTS[L] * letter_mult
        if isinstance(sq, anchor) and sq is not ANY and direction is not DOWN:
            crosstotal += cross_word_score(board, L, (i,j), other_direction)
    return crosstotal + word_mult * total

def cross_word_score(board, L, pos, direction):
    "Return the score of a word made in the other direction from the msin eord"
    i, j = pos
    (j2, word) = find_cross_word(board, i, j)
    return calculate_score(board, (i, j2), DOWN, L, word.replace('.', L))

def bonus_template(quadrant):
    "Make a board from the upper-left quadrant."
    return mirror(map(mirror, quadrant.split()))

def mirror(sequence): return sequence + sequence[-2::-1]

SCRABBLE = bonus_template("""
|||||||||
|3..:...3
|.2...;..
|..2...:.
|:..2...:
|....2...
|.;...;..
|..:...:.
|3..:...*
""")

WWF = bonus_template("""
|||||||||
|...3..;.
|..:..2..
|.:..:...
|3..;...2
|..:...:.
|.2...3..
|;...:...
|...:...*
""")

BONUS = WWF

DW, TW, DL, TL = '23:;' 

def show(board):
    "Print the board."
    for j, row in enumerate(board):
        for i, sq in enumerate(row):
            print (sq if (is_letter(sq) or sq == '|') else BONUS[j][i]),
        print
    return None

#show(a_board())

def make_play(play, board):
    "Put the word down on the board."
    (score, (i, j), (di, dj), word) = play
    for n, letter in enumerate(word):
        board[j+n*dj][i+n*di] = word[n]
    return board

def best_play(hand, board):
    "Return the highest-scoring play.  Or None."
    plays = all_plays(hand, board)
    return sorted(plays)[-1] if plays else NOPLAY
        
NOPLAY = None

def show_best(hand, board):
    print 'Current board:'
    show(board)
    play = best_play(hand, board)
    if play:
        print '\nNew word: %r scores %d' % (play[-1], play[0])
        show(make_play(play, board))
    else:
        print 'Sorry, no legal plays'

#show(make_play((30, (13,2), (1,0), 'KIN'), a_board()))

##def all_plays2(hand, board):
##    """All plays in both directions. A play is a (pos, dir, word) tuple,
##    where pos is an (i, j) pair, and dir is ACROSS or DOWN."""
##    hplays = horizontal_plays(hand, board)            # set of ((i, j), word)
##    vplays = horizontal_plays(hand, transpose(board)) # set of ((j, i), word)
##    results = set()
##    results = results|set(((i, j), ACROSS, word) for ((i,j), word) in hplays)
##    results = results|set(((j, i), DOWN, word) for ((i,j), word) in vplays)
##    return results
##
##show(a_board())
##print timedcall(all_plays, a_hand, a_board())
##print timedcall(all_plays2, a_hand, a_board())





