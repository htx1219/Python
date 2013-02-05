import sys
import itertools
from Crypto.Cipher import AES

key1 = "140b41b22a29beb4061bda66b6747e14"
c1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"

A0 = "9d1a4f78cb28d863"
A1 = "75e5e3ea773ec3e6"
B0 = "9f970f4e932330e4"
B1 = "6068f0b1b645c008"
C0 = "5f67abaf5210722b"
C1 = "bbe033c00bc9330e"
D0 = "4af532671351e2e1"
D1 = "87a40cfa8dd39154"



def convert_to_bits(n,pad):
    result = [ ]
    while n > 0:
        if n % 2 == 0:
            result = [0] + result
        else:
            result = [1] + result
        n = n / 2
    while len(result) < pad:
        result = [0] + result
    return result 

def string_to_bits(s):
    result = [ ]
    for c in s:
        result = result + convert_to_bits(ord(c),8) 
    return ''.join([str(p) for p in result])

def convert_to_hex(n):
    if n in ["a","b","c","d","e","f"]:
        n = ord(n)-87
    else:
        n = int(n)
    q = "".join([str(p) for p in convert_to_bits(n,4)])
    return q

def bit_to_hex(n):
    assert len(n) == 4
    q = sum([int(n[k])*2**(3-k) for k in range(4)])
    if q >=10:
        q = chr(q+87)
    else:
        q = str(q)
    return q

def bits_to_hex(n):
    assert len(n)%4 == 0
    dig = len(n)/4
    q = []
    for i in range(dig):
        q.append(bit_to_hex(n[4*i:4*i+4]))
    return "".join(q)

def hexs_to_bits(s):
    return "".join([str(convert_to_hex(p)) for p in s])

def xor(p, q):
    if len(p)!=len(q):
        print p, q
        raise AssertionError
    k = [0]*len(p)
    for i in range(len(p)):
        k[i] = (int(p[i])+int(q[i])) % 2
    return "".join([str(m) for m in k])

def hexxor(p,q):
    return xor(hexs_to_bits(p),hexs_to_bits(q))

def bits_to_char(b):
    assert len(b) == 8
    value = 0
    for e in b:
        value = (value * 2) + int(e)
    return chr(value)

def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + 8]) 
                    for i in range(0, len(b), 8)])

p = itertools.product("0123456789abcdef",repeat=2)
keys = list(p)
def decryp(n):
    res = []
    for key in keys:
        k = "".join(key)
        cor = True
        for msg in MSGS:
            t = hexxor(msg[2*n:2*n+2],k)
            q = sum([int(t[i])*2**(7-i) for i in range(8)])
            if q<32 or q>128:
               cor = False
        if cor:
            res.append(k)
    return res

valid_char1 = [32,33,34,39,40,41,44,45,46,63,93]+range(48,59)+range(65,91)+range(93,123)
valid_char = range(0, 127)
valid_char2 = valid_char1+range(128,256) 
brute= 0

print xor(hexs_to_bits(A1), hexs_to_bits(A0))
print xor(hexs_to_bits(B1), hexs_to_bits(B0))
print xor(hexs_to_bits(C1), hexs_to_bits(C0))
print xor(hexs_to_bits(D1), hexs_to_bits(D0))

def valid_bits(n):
    assert len(n)%8 == 0
    valid = True
    for i in range(0,len(n),8):
        w = n[i:i+8]
        q = sum([int(w[i])*2**(7-i) for i in range(8)])
        if brute == 1:
            valid_char_list = valid_char
        elif brute == 0:
            valid_char_list = valid_char1
        elif brute == 2:
            valid_char_list = range(0,128)
        elif brute == 3:
            valid_char_list = range(0,256)
        elif brute == 4:
            valid_char_list = valid_char2
        if q not in valid_char_list:
            return False
    return True

c1_s=bits_to_string(hexs_to_bits(c1))
iv = c1_s[0:16]
k1=AES.new(bits_to_string(hexs_to_bits(key1)), AES.MODE_ECB)
q = k1.decrypt(c1_s[16:32])
ans = bits_to_string(xor(string_to_bits(q), string_to_bits(iv)))
print ans
