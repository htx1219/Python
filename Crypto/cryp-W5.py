import math  # Use sqrt, floor

def gcd(a,b):
	"""gcd(a,b) returns the greatest common divisor of the integers a and b."""
	if a == 0:
		return b
	return abs(gcd(b % a, a))
	
def powmod(b,e,n):
	"""powmod(b,e,n) computes the eth power of b mod n.  
	(Actually, this is not needed, as pow(b,e,n) does the same thing for positive integers.
	This will be useful in future for non-integers or inverses."""
	accum = 1; i = 0; bpow2 = b
	while ((e>>i)>0):
		if((e>>i) & 1):
			accum = (accum*bpow2) % n
		bpow2 = (bpow2*bpow2) % n
		i+=1
	return accum
	
def xgcd(a,b):
	"""xgcd(a,b) returns a list of form [g,x,y], where g is gcd(a,b) and
	x,y satisfy the equation g = ax + by."""
	a1=1; b1=0; a2=0; b2=1; aneg=1; bneg=1; swap = False
	if(a < 0):
		a = -a; aneg=-1
	if(b < 0):
		b = -b; bneg=-1
	if(b > a):
		swap = True
		[a,b] = [b,a]
	while (1):
		quot = -(a / b)
		a = a % b
		a1 = a1 + quot*a2; b1 = b1 + quot*b2
		if(a == 0):
			if(swap):
				return [b, b2*bneg, a2*aneg]
			else:
				return [b, a2*aneg, b2*bneg]
		quot = -(b / a)
		b = b % a;
		a2 = a2 + quot*a1; b2 = b2 + quot*b1
		if(b == 0):
			if(swap):
				return [a, b1*bneg, a1*aneg]
			else:
				return [a, a1*aneg, b1*bneg]

p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
q = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333

"""find x that g**x mod p == h"""
def find(p, g, h, B= 2**20):
    d = {}
    w = powmod(g, B, p)
    for i in range(B):
        j = powmod(g,i,p)
        m,a,b = xgcd(j,p)
        d[h*a % p] = i
    print "first part complete"
    for j in range(B):
        n = powmod(w, j, p)
        if n in d:
            print "the answer is", j*B + d[n]
            break

find(13, 2, 5, 8)
#find(p, q, h)
"""the answer is 375374217830"""

p = 1267650600228229401496703205223 

print math.log(p, 2)
g = 3

 
g_a = 142621255265782287951127214876
g_b = 609743693736442153553407144551

#find(p, g, g_a)
"""the answer is 6301760"""
a = 6301760

print powmod(g, a, p)
print powmod(g_b, a, p)
