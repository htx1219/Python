import urllib2
import sys

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
    return bits_to_hex(xor(hexs_to_bits(p),hexs_to_bits(q)))

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

def string_xor_to_hex(p,q):
    return bits_to_hex(xor(string_to_bits(p), string_to_bits(q)))

def string_to_hex(q):
    return bits_to_hex(string_to_bits(q))

def num_to_hex(x):
    return bits_to_string(convert_to_bits(x,8))

q = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
def query(q):
    target = TARGET + urllib2.quote(q)    # Create query URL
    req = urllib2.Request(target)         # Send HTTP request to server
    try:
        f = urllib2.urlopen(req)
        print q # Wait for response
    except urllib2.HTTPError, e:          
        print "We got: %d" % e.code       # Print response code
        if e.code == 404:
            return True # good padding
        return False # bad padding

l = len(q)

correct = 'sifrage'+chr(9)*9
j = 17

q = q[:96]

l = len(q)
correct = 'queamish Os'
s = 12

for j in range(s, 17):
    for i in range(1, 128):
        guess = chr(i)+correct
        pad = chr(j)*j
        print guess, pad
        assert len(pad) == len(guess)
        new_c = q[:(l-32)-2*len(pad)] + hexxor(string_xor_to_hex(pad, guess), q[(l-32)-2*len(pad):l-32])+q[l-32:]
        print new_c
        if query(new_c):
            correct = chr(i)+correct
            print "We got the right one!"
            print correct, i
            break
    
print correct

correct = "The Magic Words are Squeamish Ossifrage"
