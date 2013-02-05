import itertools
import math

C1 = "1010110010011110011111101110011001101100111010001111011101101011101000110010011000000101001110111010010111100100111101001010000011000001010001001001010000000010101001000011100100010011011011011011010111010011000101010111111110010011010111001001010101110001111101010000001011110100000000010010111001111010110000001101010010110101100010011111111011101101001011111001101111101111000100100001000111101111011011001011110011000100011111100001000101111000011101110101110010010100010111101111110011011011001101110111011101100110010100010001100011001010100110001000111100011011001000010101100001110011000000001110001011101111010100101110101000100100010111011000001111001110000011111111111110010111111000011011001010010011100011100001011001101110110001011101011101111110100001111011011000110001011111111101110110101101101001011110110010111101000111011001111"

C2 = "1011110110100110000001101000010111001000110010000110110001101001111101010000101000110100111010000010011001100100111001101010001001010001000011011001010100001100111011010011111100100101000001001001011001110010010100101011111010001110010010101111110001100010100001110000110001111111001000100001001010100011100100001101010101111000100001111101111110111001000101111111101011001010000100100000001011001001010000101001110101110100001111100001011101100100011000110111110001000100010111110110111010010010011101011111111001011011001010010110100100011001010110110001001000100011011001110111010010010010110100110100000111100001111101111010011000100100110011111011001010101000100000011111010010110111001100011100001111100100110010010001111010111011110110001000111101010110101001110111001110111010011111111010100111000100111001011000111101111101100111011001111"

#####
# CHANGE THESE VARIABLES

plaintext1 = """Anyone who considers arithmetical methods of producing
random digits is, of course, in a state of sin. (John von Neumann)"""
plaintext2 = """I visualize a time when we will be to robots what dogs
are to humans, and I'm rooting for the machines.  (Claude Shannon)"""


def xor_bit(x1, x2):
    return int(not x1 == x2)

def xor(t1, t2):
    try:
        assert len(t1) == len(t2)
    except AssertionError:
        print len(t1), len(t2), t1, t2
    result = []
    for i in range(len(t1)):
        result.append(xor_bit(t1[i], t2[i]))
    return ''.join(str(x) for x in result)

# END
#############

#############
# Below is some code that might be useful
#

BITS = ('0', '1')
ASCII_BITS = 7

def display_bits(b):
    """converts list of {0, 1}* to string"""
    return ''.join([BITS[e] for e in b])

def seq_to_bits(seq):
    return [0 if b == '0' else 1 for b in seq]

def pad_bits(bits, pad):
    """pads seq with leading 0s up to length pad"""
    assert len(bits) <= pad
    return [0] * (pad - len(bits)) + bits
        
def convert_to_bits(n):
    """converts an integer `n` to bit array"""
    result = []
    if n == 0:
        return [0]
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return pad_bits(result, ASCII_BITS)

def string_to_bits(s):
    def chr_to_bit(c):
        return pad_bits(convert_to_bits(ord(c)), ASCII_BITS)
    return [b for group in 
            map(chr_to_bit, s)
            for b in group]

def bits_to_char(b):
    assert len(b) == ASCII_BITS
    value = 0
    for e in b:
        value = (value * 2) + int(e)
    return chr(value)

def list_to_string(p):
    return ''.join(p)

def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + ASCII_BITS]) 
                    for i in range(0, len(b), ASCII_BITS)])

def bits_to_int(b):
    assert len(b) == ASCII_BITS
    value = 0
    for e in b:
        value = (value * 2) + int(e)
    return value

def bits_to_ints(b):
    return ([bits_to_int(b[i:i + ASCII_BITS])
             for i in range(0, len(b), ASCII_BITS)])

c = ''.join(str(x) for x in string_to_bits('LIUHAINAN'))
q = xor(C1, C2)

def decipher(C1, key):
    m = xor(C1, key)
    q = bits_to_ints(m)
    return m, min(q), bits_to_string(m)

LETTERS = """ ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,()?"'-"""

def count_vowels(C1):
    q = bits_to_ints(C1)
    x = [q.count(ord(x)) for x in 'AEIOUaeiou']
    return 100.*sum(x)/len(q)

def count_letters(C1):
    q = bits_to_ints(C1)
    l = [q.count(ord(x)) for x in LETTERS]
    w = len(q)
    return 100.*sum(l)/w

def find_word_s(word, t1 = C1, t2 = C2):
    word_len = len(word)
    for i in range(len(t1)/7-word_len):
        #keys = itertools.product('01', repeat = 35)
        part_t1 = t1[7*i:7*i+7*word_len]
        part_t2 = t2[7*i:7*i+7*word_len]
        m1 = word
        bits1 = ''.join(str(x) for x in string_to_bits(m1))
        key = xor(part_t1, bits1)
        bits2 = xor(part_t2, key)
        m2 = bits_to_string(bits2)
        if min([(x in LETTERS) for x in m2]) == 1:
            print m2, key, i

def find_word(word, t1 = C1, t2 = C2):
    word_len = len(word)
    for i in range(len(t1)/7-word_len):
        #keys = itertools.product('01', repeat = 35)
        part_t1 = t1[7*i:7*i+7*word_len]
        part_t2 = t2[7*i:7*i+7*word_len]
        m1 = word
        bits1 = ''.join(str(x) for x in string_to_bits(m1))
        key = xor(part_t1, bits1)
        bits2 = xor(part_t2, key)
        m2 = bits_to_string(bits2)
        bits2, min_ints2, mn = decipher(part_t2, key)
        l2 = count_letters(bits2)
        #if min_ints2 >= 32:
            print m2, key, i

common100 = {1: 'the', 2: 'of', 3: 'and', 4: 'a', 5: 'to', 6: 'in', 7: 'is',
             8: 'you', 9: 'that', 10: 'it', 11: 'he', 12: 'was', 13: 'for',
             14: 'on', 15: 'are', 16: 'as', 17: 'with', 18: 'his', 19: 'they',
             20: 'I', 21: 'at', 22: 'be', 23: 'this', 24: 'have', 25: 'from',
             26: 'or', 27: 'one', 28: 'had', 29: 'by', 30: 'word', 31: 'but',
             32: 'not', 33: 'what', 34: 'all', 35: 'were', 36: 'we',
             37: 'when', 38: 'your', 39: 'can', 40: 'said', 41: 'there',
             42: 'use', 43: 'an', 44: 'each', 45: 'which', 46: 'she', 47: 'do',
             48: 'how', 49: 'their', 50: 'if', 51: 'will', 52: 'up',
             53: 'other', 54: 'about', 55: 'out', 56: 'many', 57: 'then',
             58: 'them', 59: 'these', 60: 'so', 61: 'some', 62: 'her',
             63: 'would', 64: 'make', 65: 'like', 66: 'him', 67: 'into',
             68: 'time', 69: 'has', 70: 'look', 71: 'two', 72: 'more',
             73: 'write', 74: 'go', 75: 'see', 76: 'number', 77: 'no',
             78: 'way', 79: 'could', 80: 'people', 81: 'my', 82: 'than',
             83: 'first', 84: 'water', 85: 'been', 86: 'call', 87: 'who',
             88: 'oil', 89: 'its', 90: 'now', 91: 'find', 92: 'long',
             93: 'down', 94: 'day', 95: 'did', 96: 'get', 97: 'come',
             98: 'made', 99: 'may', 100: 'part'}



def find_100():
    for i in range(1, 100):
        print common100[i]
        find_word_s(' '+ common100[i]+' ')
        find_word_s(' '+ common100[i] + ', ')
        find_word_s(' '+ common100[i] + '. ')
        

def brute_force(n, t1=C1,t2= C2):
    keys = itertools.product('01', repeat = n*7)
    print math.log10(2**(n*7))
    i = 0
    for key in keys:
        i += 1
        if i % 20000 == 0:
            print 'iters number: ', i
        bits1, min_ints1, m1 = decipher(t1[:n*7], key)
        bits2, min_ints2, m2 = decipher(t2[:n*7], key)
        v1 = count_vowels(bits1)
        v2 = count_vowels(bits2)
        l1 = count_letters(bits1)
        l2 = count_letters(bits2)
        if min_ints1 < 32: continue
        if min_ints2 < 32: continue
        if v1 < 20: continue
        if v2 < 20: continue
        if l1 < 90: continue
        if l2 < 90: continue
        print m1, m2, key
    

