import sys
import itertools
from Crypto.Cipher import AES
import hashlib

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt=make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

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

t=open("test.mp4","rb")
t = t.read()
print len(t)
q=open("quiz.mp4","rb")
q = q.read()
print len(q)

def largefile(t):
    k = range(0, len(t), 1024)
    k.reverse()
    h = len(k) *[0]
    h[0] = hashlib.sha256(t[k[0]:]).digest()
    print len(t[k[0]:])
    print list(enumerate(k))[-1]
    for (i, f) in enumerate(k):
        if i != 0:
            h[i] = hashlib.sha256(t[k[i]:k[i-1]]+h[i-1]).digest()
    return bits_to_hex(string_to_bits(h[-1])), h

print largefile(t)[0]
