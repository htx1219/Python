BITS = ('0', '1')
ASCII_BITS = 8
 
def pad_to_block(bits, block_size):
    if len(bits) % block_size == 0:
        return bits
    else:
        return pad_bits(bits, block_size * (len(bits) / block_size + 1))
 
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
    return result
 
def string_to_bits(s):
    def chr_to_bit(c):
        return pad_bits(convert_to_bits(ord(c)), ASCII_BITS)
    return [b for group in
            map(chr_to_bit, s)
            for b in group]
 
def bits_to_int(b):
    value = 0
    for e in b:
        value = (value * 2) + e
    return value
 
def bits_to_char(b):
    assert len(b) == ASCII_BITS
    value = bits_to_int(b)
    return chr(value)
 
def list_to_string(p):
    return ''.join(p)
 
def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + ASCII_BITS])
                    for i in range(0, len(b), ASCII_BITS)])
