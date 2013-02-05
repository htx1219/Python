sec = [4292994350, 1536389295, 4042431367, 3384302645, 2035141728, 3694012268, 2800106660, 387169270, 1931368155, 2313027219, 2401988609, 4009711196, 2511867215, 2141921935, 3691424850, 3583068679, 55981814, 3366258802, 2870675337, 1384398332, 2374224221, 1109324721, 3252986718, 259642665, 4065436664, 3169491215, 684847233, 1967950918, 1761103132, 2789617314, 2082902972, 588732123, 323601286, 2343264793, 2766261905, 3585151325, 1894204746, 3632833394, 1940040064, 1146207988, 3511993505, 685735866, 2858571120, 1874842012, 824884701, 3756573615, 2506023712, 4100053623, 2943458514, 820854338, 3100538591, 1990141088, 1731949124, 1334992291, 2646157195, 3375289919, 3700673110, 2540372588, 1239758838, 3045145299, 4070309820, 3231542850, 1308607425, 1320625912, 4292994350, 1536389295, 4042431367, 3384302645, 2035141728, 3694012268, 2800106660, 387169270, 1931368155, 2313027219, 2401988609, 4009711196, 2511867215, 2141921935, 3691424850, 3583068679, 55981814, 3366258802, 2870675337, 1384398332, 2374224221, 1109324721, 3252986718, 259642665, 4065436664, 3169491215, 684847233, 1967950918, 1761103132, 2789617314, 2082902972, 588732123, 323601286, 2343264793, 2766261905, 3585151325, 1894204746, 3632833394, 1940040064, 1146207988, 3511993505, 685735866, 2858571120, 1874842012, 824884701, 3756573615, 2506023712, 4100053623, 2943458514, 820854338, 3100538591, 1990141088, 1731949124, 1334992291, 2646157195, 3375289919, 3700673110, 2540372588, 1239758838, 3045145299, 4070309820, 3231542850]
print len(sec)

BITS = ('0', '1')
ASCII_BITS = 8

def display_bits(b):
    """converts list of {0, 1}* to string"""
    return ''.join([BITS[e] for e in b])

def seq_to_bits(seq):
    return [0 if b == '0' else 1 for b in seq]

def pad_bits(bits, pad):
    """pads seq with leading 0s up to length pad"""
    assert len(bits) <= pad
    return [0] * (pad - len(bits)) + bits

def bits_to_dec(s):
    return sum([int(s[i])*2**(len(s)-i-1) for i in range(len(s))])
       
def convert_to_bits(n):
    """converts an integer `n` to bit array"""
    result = []
    if n == 0:
        return [0]
    while n > 0:
        result = [(n % 2)] + result
        n = n / 2
    return result

def xor(p,q):
    assert len(p) == len(q)
    return [int(p[i] != q[i]) for i in range(len(p))]

bits_sec = [display_bits(pad_bits(convert_to_bits(num), 32)) for num in sec]
max_len = 32

long_str = "".join(bits_sec)
print len(long_str)

for i in range(0,len(long_str), 57):
    print long_str[i:i+57]
    print bits_to_int(seq_to_bits(long_str[i:i+57]))



def compute_neibor(bits_sec):
    bits_nei = []
    for i in range(len(bits_sec)-1):
        n_bits = xor(pad_bits(seq_to_bits(bits_sec[i]),32), pad_bits(seq_to_bits(bits_sec[i+1]),32))
        bits_nei.append(display_bits(n_bits))

    for i in bits_nei:
        print i

    return bits_nei

##bits_1_nei = compute_neibor(bits_sec)
##
##print "BITS 1"
##
##bits_2_nei = compute_neibor(bits_1_nei)

def gen_random_seq(seed, n):
    seq = []
    state = seed
    for unused in range(n):
        extract = [state[i] for i in range(0, len(state), 2)]
        seq.append(bits_to_dec(extract))
        for i in range(387):
            bits_inc(state)
        bits_rotate(state, 7)
    return seq

def bits_inc(bits):
    """modifies `bits` array in place to increment by one
    
    wraps back to zero if `bits` is at its maximum value (each bit is 1)
    """
    # start at the least significant bit and work towards
    # the most significant bit
    for i in range(len(bits) - 1, -1, -1):
        if bits[i] == 0:
            bits[i] = 1
            break
        else:
            bits[i] = 0

def find_seed(n):
    for i in range(n):
        s = gen_random_seq(i, 1)
        if s[0] == 4292994350:
            print "Find it! the seed is ", i
            return i

find_seed
