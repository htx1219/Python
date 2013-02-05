import urllib
import json
import base64

BLOCK_SIZE = 128
site = "http://cs387.udacity-extras.appspot.com/beast"

def unencode_json(txt):
    d = json.loads(txt)
    return dict((str(k),
                 base64.urlsafe_b64decode(str(v)))
                for k,v in d.iteritems())

def _send(attack=None, token=None):
    data = {}
    if attack is not None:
        data["attack"] = base64.urlsafe_b64encode(attack)
    if token is not None:
        data["token"] = base64.urlsafe_b64encode(token)

    # here we make a post request to the server, sending
    # the attack and token data
    json = urllib.urlopen(site, urllib.urlencode(data)).read()
    json = unencode_json(json)
    return json
    
_TOKEN = None
def send(attack=None):
    """send takes a string (representing bytes) as an argument 
    and returns a string (also, representing bytes)"""
    global _TOKEN
    json = _send(attack, _TOKEN)
    _TOKEN = json["token"]
    return json["message"]

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

def xor(p, q):
    if len(p)!=len(q):
        print p, q
        raise AssertionError
    k = [0]*len(p)
    for i in range(len(p)):
        k[i] = (int(p[i])+int(q[i])) % 2
    return "".join([str(m) for m in k])

def bits_to_char(b):
    assert len(b) == 8
    value = 0
    for e in b:
        value = (value * 2) + int(e)
    return chr(value)

def bits_to_string(b):
    return ''.join([bits_to_char(b[i:i + 8]) 
                    for i in range(0, len(b), 8)])

def sxor(p, q):
    return bits_to_string(xor(string_to_bits(q), string_to_bits(p)))

sth = "attack at dawn. "
ans = 'What hath God wr'
def decrypt(n):
    assert len(sth) == 16
    print 'attack start'
    attack = sth[:15-n]
    k0 = send(attack)
    iv0 = k0[-16:]
    k1 = send(attack)
    iv1 = k1[-16:]
    for i in range(97, 128)+[32]+range(65, 97)+range(32, 65):
        print i
        ori_m = attack+ans+chr(i)
        p = sxor(sxor(iv1, iv0), ori_m)
        k2 = send(p)
        iv1 = k2[-16:]
        if k2[:16] == k1[:16]:
            print chr(i)
            return chr(i)

def find_all(start = 0):
    global ans
    for i in range(start, 16):
        k = decrypt(i)
        ans += k
        print ans

#find_all()

def decrypt2(n):
    assert len(sth) == 16
    print 'attack start'
    attack = sth[:15-n]
    k0 = send(attack)
    iv0 = k0[-16:]
    k1 = send(attack)
    iv1 = k1[-16:]
    for i in range(97, 128)+[32]+range(65, 97)+range(32, 65):
        print i
        ori_m = attack+ans+chr(i)
        p = sxor(sxor(iv1, iv0), ori_m[:16])
        k2 = send(p+ori_m[16:])
        iv1 = k2[-16:]
        if k2[16:32] == k1[16:32]:
            print chr(i)
            return chr(i)

def find_all(start = 0):
    global ans
    for i in range(start, 16):
        k = decrypt2(i)
        ans += k
        print ans

find_all()

secret_message = "What hath God wrought? -Samuel Morse"
