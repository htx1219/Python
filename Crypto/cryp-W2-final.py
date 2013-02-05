import sys
import itertools
from Crypto.Cipher import AES

key1 = "140b41b22a29beb4061bda66b6747e14"
c1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
c2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"

key2 = "36f18357be4dbd77f050515c73fcf9f2"
c3 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
c4 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"

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

def bits_to_int(s):
    return sum([int(s[i])*2**(len(s)-i-1) for i in range(len(s))])

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

i=0
c1_s=bits_to_string(hexs_to_bits(c1))
k1=AES.new(bits_to_string(hexs_to_bits(key1)), AES.MODE_ECB)
iv = c1_s[i:i+16]
q = k1.decrypt(c1_s[i+16:i+32])
ans = bits_to_string(xor(string_to_bits(q), string_to_bits(iv)))
print ans

def cbc(key1, c1):
    c1_s=bits_to_string(hexs_to_bits(c1))
    k1=AES.new(bits_to_string(hexs_to_bits(key1)), AES.MODE_ECB)
    res = ""
    for i in range(0, len(c1_s)-16, 16):
        iv = c1_s[i:i+16]
        q = k1.decrypt(c1_s[i+16:i+32])
        print res, i, len(q),len(iv)
        ans = bits_to_string(xor(string_to_bits(q), string_to_bits(iv)))
        print ans, len(ans), ord(ans[-1])
        res = res+ans
    return res
        
print cbc(key1, c1)
print cbc(key1, c2)


c3_s=bits_to_string(hexs_to_bits(c3))
k=AES.new(bits_to_string(hexs_to_bits(key2)), AES.MODE_ECB)
iv = bits_to_int(string_to_bits(c3_s[0:16]))
d_k = k.encrypt(c3_s[0:16])
print bits_to_string(xor(string_to_bits(d_k), string_to_bits(c3_s[16:32])))


def ctrmode(key, c):
    c_s=bits_to_string(hexs_to_bits(c))
    k=AES.new(bits_to_string(hexs_to_bits(key)), AES.MODE_ECB)
    iv = bits_to_int(string_to_bits(c_s[0:16]))
    d_k = ""
    for i in range(0, len(c_s)-16, 16):
        q = "".join([str(i) for i in convert_to_bits(iv+i/16, 128)])
        d_k = d_k + k.encrypt(bits_to_string(q))
    k = len(c_s[16:])
    return bits_to_string(xor(string_to_bits(d_k[:k]), string_to_bits(c_s[16:])))

print ctrmode(key2, c3)
print ctrmode(key2, c4)

p = bits_to_hex(xor(string_to_bits("Pay Bob 100$"), string_to_bits('Pay Bob 500$')))
print p
iv = "20814804c1767293b99f1d9cab3bc3e7"
