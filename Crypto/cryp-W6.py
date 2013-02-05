import math  # Use sqrt, floor
import gmpy

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

N1 = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581

N2 = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877

N3 = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929

def find1(N, A = None):
    if A == None:
        A = gmpy.mpz(gmpy.sqrt(N)+1)
    k = A*A - N
    assert gmpy.is_power(k)
    x = gmpy.sqrt(A*A - N)
    p, q =  A - x, A + x
    print p
    print q
    assert gmpy.is_prime(p)
    assert gmpy.is_prime(q)
    assert p*q==N
    return p, q

find1(N1)

def find2(N):
    A = gmpy.mpz(gmpy.sqrt(N)+1)
    while True:
        try:
            find1(N, A)
            return
        except:
            A = A+1
            pass

find2(N2)

def find3(N, A = None):
    if A == None:
        A = gmpy.mpz(gmpy.sqrt(24*N)+1)
    k = A*A - 24*N
    assert gmpy.is_power(k)
    x = gmpy.sqrt(k)
    print x
    q1 =  (A - x)/4
    p1 = (A + x)/6

    q2 = (A + x)/4
    p2 = (A - x)/6
    
    if gmpy.is_prime(p1) and gmpy.is_prime(q1) and p1*q1==N:
        print p1
        print q1
    elif gmpy.is_prime(p2) and gmpy.is_prime(q2) and p2*q2==N:
        print p2
        print q2
    else:
        assert False
        
def find4(N):
    A = gmpy.mpz(gmpy.sqrt(6*N)+1)
    while True:
        try:
            find3(N, A)
            return
        except:
            A = A+1
            pass

#find3(N3)
#find4(N3)

c = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

def rsa(c):
    p, q = find1(N1)
    f = N1 - p - q + 1
    e = 65537
    g, d, y = xgcd(e, f)
    print g, d*e % f
    pt = powmod(c, d, N1)
    bpt = convert_to_bits(pt, 2048)
    hpt = bits_to_hex(bpt)
    print hpt
    print len(hex(pt))

rsa(c)

tar_pt = int(0x466163746f72696e67206c65747320757320627265616b205253412e)
print hex(tar_pt)
print bits_to_string(convert_to_bits(tar_pt, 28*8))


e = 65537
n = 132177882185373774813945506243321607011510930684897434818595314234725602493934515403833460241072842788085178405842019124354553719616350676051289956113618487539608319422698056216887276531560386229271076862408823338669795520077783060068491144890490733649000321192437210365603856143989888494731654785043992278251

################
# Here are two example signatures
#
# First message
m1 = 387
# first signature
s1 = 104694095966994423550399840405679271451689287439740118881968798612714798360187905616965324945306116261186514828745033919423253353071142760352995900515279740753864505327750319034602409274084867637277266750899735986681083836544151016817569622466120342654469777762743360212628271549581658814852850038900877029382

# Second message
m2 = 2
# second signature
s2 = 18269259493999292542402899855086766469838750310113238685472900147571691729574239379292239589580462883199555239659513821547589498977376834615709314449943085101697266417531578751311966354219681199183298006299399765358783274424349074040973733214578342738572625956971005052398172213596798751992841512724116639637
