# For this problem, Alice and Bob want to communicate
# They have set up two servers to respond to messages
# and you need to transfer the messages between the two.
#
# The protocol goes as follows:
# 1) a. Establish a session with Alice
#    b. Establish a session with Bob
# 2) a. Send Alice's public information to Bob
#    b. Send Bob's public information to Alice
# 3) Relay messages
#
# Step 1 - Establishing a session
# The function `initialize` can be used to establish a session.
# Alice responds to a POST request with the `type` key set to "init".
# She will send back two values: a token which is used to track the 
# session and a public value, g^x.  The token will expire after 20 minutes,
# so you will need to re-initialize a session after that time
#
# Step 2 - Exchanging public information
# Alice now needs Bob's public value.  The function `send_key` can be
# used to send this.  The function makes a POST request.  Alice responds with 
# a successful status.
#
# Step 3 - Relay messages
# Now that Alice and Bob have a shared secret key, they can use that
# to encrypt secret messages.  You will need to relay these messages.
# Use the `recieve_msg` function to get the first message to send from Alice
# Then, take the values recieved from that and send them to Bob, who will
# respond.  Take his response and send it back to Alice.  Repeat.
#
# Errors
# If you try to do something that Alice and Bob don't like, for example sending a message
# without first exchanging public information, they will respond with 
# a 501 status code and more information in the response.
#
# As with the challenge problem of Unit 5, this assignment requires that
# you run code on your own environment.  It will not work if you write
# code in the Udacity IDE and hit RUN or SUBMIT.
#
# You're allowed to use whatever programming language you want.  The 
# code provide below can be used as a reference implementation.
#

from urllib import urlopen, urlencode
from cryp_RSA import *
from Crypto.Cipher import AES
from Crypto.Util import Counter
from hashlib import sha1
import json
import binascii


base = "http://cs387.udacity-extras.appspot.com/final"
Alice = base + "/alice"
Bob = base + "/bob"
Betty = base + '/betty'
Alex = base + '/alex'
Eve = base + '/eve'

def check_output(output):
    data = output.read()
    if output.getcode() != 200:
        raise Exception(data)
    data = json.loads(data)
    return data

def get_pg():
    output = urlopen(base)
    data = check_output(output)
    # returns {"p":<large prime>, "g":<generator for p>}
    return data

def initialize(person):
    data = {'type':'init'}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # returns a dictionary 
    # {"token":<token_value>, "public": <g^x>}
    return data

def send_key(person, token, public, name):
    """
    person: url of Alice/Bob
    token: token used to track session
    public: the public value of the other party
    name: the name of the other party - "alice", "bob"
    """
    data = {'type':'key',
            'token':token,
            'public':public,
            'name':name}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # Should be a response {"status":"success"}
    return data

def recieve_msg(person, token):
    data = {'type':'msg',
            'token':token}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # should be a response
    # {"msg":<cipher>, "iv":<initialization vector>}
    return data

def send_msg(person, token, cipher, iv):
    data = {'type':'msg',
            'token':token,
            'message':cipher,
            'iv':iv}
    output = urlopen(person, urlencode(data))
    data = check_output(output)
    # If the person doesn't have
    # a response to the message, the response will
    # just be {"status":"success"}
    # else, the response will be {"status":"sucess", 
    #                             "reply":{"msg":<cipher>,
    #                                      "iv":<initialization vector>}}
    return data

def hash(bits):
    h = sha1(bits_to_string(bits)).digest()
    return h

def find_msg(p_a, a_name, p_b, b_name):
    a = initialize(p_a)
    pg = get_pg()
    b = initialize(p_b)
    print a, b
    print pg
    s1 = send_key(p_a, a['token'], b['public'], b_name)
    s2 = send_key(p_b, b['token'], a['public'], a_name)
    print s1, s2
    k = recieve_msg(p_a, a['token'])
    print k
    while True:
        k = send_msg(p_b, b['token'], k['msg'], k['iv'])['reply']
        print k
        k = send_msg(p_a, a['token'], k['msg'], k['iv'])['reply']
        print k

msg = """Eve: I need your help.  My friends Alex and Betty are also using
Diffie Hellman to exchange a key and then send encrypted messages.  I think
that Betty and Bob have a hint; can you find it for me?  I've given you the
information I know about their system:
http://cs387.udacity-extras.appspot.com/pdf/final_challenge.pdf.
Hopefully you can find a way to break it.  Alex is also trying to help me.
Can you arrange for him and I to exchange messages?
Thanks so much for your help."""

def decrpy_msg(p_a, a_name, p_b, b_name):
    a = initialize(p_a)
    pg = get_pg()
    b = initialize(p_b)
    #print a, b
    #print pg
    s1 = send_key(p_a, a['token'], u'1', b_name)
    s2 = send_key(p_b, b['token'], u'1', a_name)
    print s1, s2
    k = recieve_msg(p_a, a['token'])
    #print k
    secret = 1
    k_hash = sha1(chr(1)).digest()
    k_a = k_hash[:16]
    k_a_nonce = k_hash[16:]
    while True:
        iv = hex_to_string(k['iv'])
        ctr = Counter.new(32, k_a_nonce+iv)
        key = AES.new(k_a, AES.MODE_CTR, 'x'*16, counter=ctr)
        print key.decrypt(hex_to_string(k['msg']))
        try:
            k = send_msg(p_b, b['token'], k['msg'], k['iv'])['reply']
        except:
            return
        #print k
        iv = hex_to_string(k['iv'])
        ctr = Counter.new(32, k_a_nonce+iv)
        key = AES.new(k_a, AES.MODE_CTR, 'x'*16, counter=ctr)
        print key.decrypt(hex_to_string(k['msg']))
        try:
            k = send_msg(p_a, a['token'], k['msg'], k['iv'])['reply']
        except:
            return
        #print k


##decrpy_msg(Bob, 'bob', Betty, 'betty')
###decrpy_msg(Bob, 'bob', Alice, 'alice')
##decrpy_msg(Bob, 'bob', Alex, 'alex')
###decrpy_msg(Alex, 'alex', Betty, 'betty')
###decrpy_msg(Alice, 'alice', Betty, 'betty')
##decrpy_msg(Alice, 'alice', Alex, 'alex')
##decrpy_msg(Alex, 'alex', Alice, 'alice')

longer_text ="""
{u'status': u'success'} {u'status': u'success'}
Hi Betty
Any hints for solving this problem?
I found a message but don't know what to do with it.
Send it to me
Okay: 8d801f00c7554d3980b0c4f400c1ebc572d86f57f48d322b8e7c3a1f01c531dbe772b77be5acd34bf1979b70089615ace253c4b01350f36f82215f164b7934fdd48a30
Thanks
{u'status': u'success'} {u'status': u'success'}
Hi Alex
Are you still using that PRNG?
Yes; but I was only able to use one LFSR
{u'status': u'success'} {u'status': u'success'}
What is the air-speed velocity of an unladen swallow?
What do you mean?  An African or European swallow?
Ok, good, it is you.  What did you find?
Bob has a PRNG he likes to use to create keys for a OTP. I found 1000 bits and put them online:http://cs387.udacity-extras.appspot.com/final/thousandbits
Thanks.  Anything else?
Also, I think he is using a PRNG similar to the A5.1 GSM
Great news.  I'll look into this
"""

what_the_fuck = "8d801f00c7554d3980b0c4f400c1ebc572d86f57f48d322b8e7c3a1f01c531dbe772b77be5acd34bf1979b70089615ace253c4b01350f36f82215f164b7934fdd48a30"

thousand_bits = [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0]

def lfsr(l, n= 50, y = False):
    ans  = []
    while len(ans)< n:
        assert len(l) == 19
        k = (l[0]+l[1]+l[2]+l[5]) % 2
        ans.append(l[0])
        l = l[1:]+[k]
        #print l
        #ans.append(k)
    return ans

##seed = [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0]
##k = lfsr(thousand_bits[:19], 120)
##a = ''.join(str(i) for i in k)
##b = ''.join(str(i) for i in thousand_bits[:120])
##print a==b
##
##c = hexs_to_bits(what_the_fuck)
##print len(c)
##
##size = 2**20
##keys = lfsr(thousand_bits[:19], size)
##for i in range(size):
##    key = keys[i:i+len(c)]
##    w = xor(key, c)
##    k = bits_to_string(w)
##    p = True
##    for char in k:
##        if ord(char)<32 or ord(char)>128:
##            p = False
##            break
##    if p:
##        print i
##        print k

the_hint = "An important question: What do you get if you multiply six by nine?"

#decrpy_msg(Alice, 'alice', Alex, 'alex')

def final_decrpy_msg(p_a = Alice, a_name = 'alice'):
    a = initialize(p_a)
    pg = get_pg()
    #print a, b
    #print pg
    s1 = send_key(p_a, a['token'], u'1', 'eve')
    print s1
    secret = 1
    k = recieve_msg(p_a, a['token'])
    k_hash = sha1(chr(1)).digest()
    k_a = k_hash[:16]
    k_a_nonce = k_hash[16:]
    while True:
        iv = hex_to_string(k['iv'])
        ctr = Counter.new(32, k_a_nonce+iv)
        key = AES.new(k_a, AES.MODE_CTR, 'x'*16, counter=ctr)
        print key.decrypt(hex_to_string(k['msg']))

        ctr = Counter.new(32, k_a_nonce+iv)
        key = AES.new(k_a, AES.MODE_CTR, 'x'*16, counter=ctr)
        w =  string_to_hex(key.encrypt(the_hint))
##        return key, ctr, w
##        print key.decrypt(hex_to_string(w))
##        print key.decrypt(key.encrypt(the_hint))
        print w
        k = send_msg(p_a, a['token'], w, k['iv'])['reply']
        print k

#final_decrpy_msg()

final_msg = """
Ah.  42, of course!  Add 'final_answer = 42' to your code and submit it.
That's it.  That's all there is.
Congrats on all your hard work in the course.  We hope you had fun.
We enjoyed putting together the class.  -Dave and Job
"""
