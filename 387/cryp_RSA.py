import math  # Use sqrt, floor
import gmpy
from hashlib import sha512

import random
import os
from Crypto.Util import number

random.seed(os.getpid())

def randfunction(N):
    # N is in bytes
    # pycrypto expects a string
    l = []
    while N > 0:
        l.append(chr(random.getrandbits(8)))
        N -= 1
    return "".join(l)

def what(i=os.getpid()):
    random.seed(i)
    p = number.getPrime(512, randfunction)
    q = number.getPrime(512, randfunction)
    n = p*q
    return p, q, n

################
e0 = 65537
n0 = 116436872704204817262873499608558046190724591466716177557829773662807162485791977636521167560986434993048860346504247233074117974671540999410485959711510256117299326339754889488213509449940603119123994148576130959569697235313003024809821145961963221161561975123663333322412762102191502543834949106445222007561
cipher0 = "<\xad\xdd\xedg\x8b\x12\x0b\x00y\xa2\xf0\x86\xcbF\xf0\x8f\xb4~\xbd\x04\xd9\xac6iwxk\xcfi\xc4Z1p\\\x14\xa4rL\x9a#\x9f\xbf~\xec[\x8d\xfc(\x82\xc2s\xb9\x0e\xec(\xd9.}\xc5\xdf\xa8'`\xa5\xdb\x18\xf1Z\xff\x82xQJa\x11\x98/x&{\x0b\x17\xb9\xb1\x88\x8f\x85B\x7fH\xdbX\x9aV\x9a\xaf\x0fKc+\xf7?\xb8\xb4\x1fo\x0eeI\xa9\x90\x11\x83\xb8\xfdaMwM\xc7\xb48&-\xe8\xf1C"
m0 = ''#YOUR ANSWER HERE
################

################
e1 = 3
n1 = 131776503472993446247578652375782286463851826883886018427615607890323792437218636575447994626809806013420405963813337101556738852432247872506699457038044621191649758706817663135648397013226104530751563478671698441687437700125203966101608457556637550910814187779205610883544935666685906870199595346450733709263
cipher1 = '\x04\xacq#E/\xf4X\x126\xef\xc6\xb1\xfc\x10p*\x98P\xde\x089K\x16y0\xfa\xde\x9f\x05\x15+\xa3\x0f\xbc3\xd1t\xe7\x9a\x1b\x04m\xa1\x12\x96\x18Y\xf9\xc95\xce\x19 E\xfa\xe1\xb5\x8a\xd5\xf2\x99\xa6"<\xcb\x1a\xd0\xce=\x91\xfbw\t\xb5'
m1 = ''#YOUR ANSWER HERE
################

################
e2 = 3
n2 = 65659232975830381768328338666607829001259240689809015666589078261348261561917417083788447204534665997091584936794919521220643455263371034991817572752104164283083678838816431044389236958346474896965382016943200300407371205608596328649170408446414718769422147103617311701247139971805834487439320773304455320217
cipher2 = '\x04\xe97r\x13\x99\xf7\x80m\x19\xe3f\x1a\x92]u!\x17\xdf\xa8\xfd\xd4\xd0\xbea\xe8\x1f\xefc\xd6\xc7\xbf\xce\xa4q\xfe\xa4S\xff\xaf\x1aX\xc13g\xeb\x12\xadw\x17T\x05\x1c\x8e\xd8\xea\x1bkc\xd3\xfctQt\x8e\xf6d\x1a\x98\xbc}\x08\x1d%\xc7\xd2K\xb4\xa8\x96\xcf\x98D\x8a\xbd\xa7\xd2\xcc\x861$\xd1\x1b\xdd\xa0h\x83\xdan\xcbm\xa4\xf9\xef\x96\x12\x9c|\xc9\xd7\t\x9b\x0f:\x9e\xe0\xa1\xb2\t\x8b\x9d\x18\x07\x8e]\x8c\x13\xa2'
m2 = ''#YOUR ANSWER HERE
################

################
e3 = 65537
n3 = 123740725722669778168140279746885116465689142044964932919259424632700251889210648897122745920893520079240373449556169792134756802777276891302849411753547670256331297747426561365967232060486102273866172732652784207074573713156422288123095681033001477048754016167961689427177649034193069903791184066398335275979
cipher3 = "\x96\x81\xd11'\xf26\xbfRx\x85\xfa*{l\xa0\xf9gN\xd5\xe1\x89\xe1$$\x0c\r\xa6\xb0\x12^X\x19gQt\xe4\xca\xb2`\xccO\xdf\xb4*\\\x12\x94\xa8\x07\xc8V2\xf2\xfa\xbd\x0f\xd9b%{\x18\x04Q\xebM\xaa\x996\xe7\xb2\xf4;\x8a\xa3\xd6t\xefi^\x9f}\xb6\xa5\xf3\xc7\x86M~b@\x06V\xa62\x99\xd5R\xb7\xaa\x8a\xd2\xd8p\xc6\xf0MU\xaf:(\xea\xa6d6!\xbb\xcd\xf96\xed\x13\xbe\xb4\xc6\x80i'"
m3 = ''#YOUR ANSWER HERE
################

################
e4 = 65537
n4 = 174231520673917075824734399421338044182598066866708821622792727890359025900245087848242723006461374386260651831496339387219798450553867568952404714118529459572066590008168303790157469082308091580819932970387450957047496109838586484814686040623994413943943700280260903054123602347796276801896181827746424409349
cipher4 = '\x8d\x15\x19\xdb\xa2b%\xa8\xf9r\xe1s\xd1\xb9\x91\x01\xac\xa5\xdbU\xac,\xcb\x89\x88\xf1i\xac\xdcC\x9dE\x18\xfeQ\xd9\xb9\xa8\xa8\x16\xafP\xdc\xd5B\x86\xb4)tK\x99\xd3\x7f\x88/\xa2\x90\xdf\xcc\x98\xa1l\xfd\xc7\xfa\x1f\xcd\x82\x1a\xf3\x98*\xb1e\xcd\xb2\xde\xae\xd6\xe8\x93hYEw?\x10\xde\xa9\x18\xc6&H\xebl\xb1\x98\x02)\x06\xf2\r\x9c`\x008\x13\xc1\xa1@\x15\x07\xf5|\x96\xdd\x84\xbd\xf9{\x8ee \xc7\x063\xb5\xb5'
m4 = ''#YOUR ANSWER HERE
################

################
e5 = 65537
n5 = 154624207324797376435320332790580937936761022444524329745992492506088072002504225456113354046488778813916771666944276555736671617396500696410754570132980562875859056165807630016963181226874989658340550960200466121814971000456664135187049322544510139273708052345814650574505699754914795663074450228533543056817
cipher5 = "i\xcf\xd3\xcd7.\xc8\xd5\x1f?\xbdtr0&z3\x1d\xf0\xe9p\xf3<YI\x80\xb0\xea3 \xb1\xda\x8e\n\x10m*\xe2\xceE\xbbi\x9c\xb5\x92\xaaMU\xe9\x1a)\x98\x07\x85\x99\xb9V\\\xbfyd\xf4T\xb3\x93\xe3N\xd8\xbd\xd8F\xde\x86Ep\xc0\xef\xd7\xe8\xc4\xf4\x80e\x16x\xcbQ\tV\xc3\xc8\xa4E\x95\xcf\x0e\xd3\\\t\xa2H\xd9\x85$vmC\x9b`\xc0\x93O MG\x0c'\xd6}\xbc\x8fO\xb6V\xcc\x1a\xcb\xc0"
m5 = ''#YOUR ANSWER HERE
################

################
e6 = 65537
n6 = 55658068259817811076952882351578415862870549608181369915628312865059323413004471043604703276316691018017425203301601197751731990108856534305858079813650908006137207122255581819587501300907072084616440442796887872335687503995776108872819766599926331124483312046239535167770356141832350688609707163033799579957
cipher6 = '",G\xae\xb7\x96 z=Y\xf3\x19\x11g\x9eA(\x8e\xa8J\x89\x86u\xb1\xd7\x8f\x86\x1e\x94\xc1GkE\xc8\x03\xe0\xb3LGN\x14\x81\xb2,\xc5\x04Z,\xe4\xf7Z\xdf\x91Z\x97\x1b]\x80\x06\xb4<\xc3x\xab\x83\x85o\x9e\x0bK\xca\x15c\x8c.O\xfb\x84\xbd>\x08\xd7\xff\r\xa6P\x86\x87)\x076\x9b\xdc\xe2\xf1\xe1`/0m\x84f\xb5\x9a\x83\xcc\xd7\x0eC\xae)\xcc\xff\xf3$<\xd6G\x17 \xb1\xd1\xe7\x1a\x0c\xac\x15\x90'
m6 = ''#YOUR ANSWER HERE
################

################
e7 = 65537
n7 = 142790458604757964122637252257956461175023701838768573868119604983049820652820576222661702788815905296939051322350625332330328946814137523526132844748550060162093126006443484056742183764004234747175547357975153233786228275781507259080966207713629148725792124704247615358292708458914175756855275828988145447879
cipher7 = "\xc7\x7f\x91'Y'\xc6_\x91N\xa4\x0e\xe0\x83PX\xe1\xd2O\xf3\xff\x1e\x95\xc5{&\x07\xd7O9\x82;\xf0U9\xf1\x9b\x9a\x8d\x1b+cX\x17-X\xc7\xb0,\xe4Z0\x84PP\x89\xbf\xa4\xc3\xf6\xa2\xec\xdf\xf3\xca\x86\xc4\xad\xcfQ\xcf\xbcW\xd9m\xb2T\x98\x9dWu\xab\x8f\xe3\x91\xccL@\x89\xcf\xcc\x1f\xed>\x98\\\x02\xefE\x84\xa3t\x1d\xd3\xf8(PkO\x17q\xf7\xafX\x10S\x94\xdf\x9a*\xbc\xb3\x00\xecYa\xc2\x16"
m7 = ''#YOUR ANSWER HERE
################

################
e8 = 3
n8 = 105242314862613403128618012971241387248892052783002974105856821061278607957729115063535600558210614458208545471459242061573520534172108013775924181710251914675571061791713994144059933046151548906145029415704879628926489802957314522493622596489433179478769931611554984108813301116133814976882152241405085792401
cipher8 = '!t\x1fF\x81\xc3\x84m\x96z_\xaf\xcf[\xbbt\xef\xac\xf7\xc9]\xebaw\x06\x0e\x8ey\\H_\xee0B\xbaB?\xa9-4\x1cd\x16\xa4\x85\xeaOO\xda\xf8\x8e;\xdbY\xb6b\xf7|\xaf\x13\xa9\xba\x9a\xc5i\xa7f\x94\x80HJ^-\x80\x96\xd9\xb5\x1e\x9b5\x1c\xe2\xfa\xbc\xb3\xb5\xfa\xffIq\xabt$\x10\x01K\xef[;\x04T\x17\n\xbf\xa7\xb4\x0fr2\x19\xc43\x19\xa9\xac\xbb\x82Y\xf4X%\x8f\x0bd\x81\xa7n\xce'
m8 = ''#YOUR ANSWER HERE
################

################
e9 = 3
n9 = 72119364642335338558230934777058054962694972953443182639333046521176125046406938854054638169330108689724380250570350428800376971990405399883726478777738596059986080075671524555383338963957060973245384873014181662159740775682510335778372893164426839838949550467826086219705472573462606617295335262085826901917
cipher9 = 'B\xc1\xd9EH\x8b\xc9D_s\x17\x90uGd\xb6\x10F\x16\xab\x1aN=t\\\xb6\xaa\xf6\x97\xd6\x17\xab&\xd1 Z\x82\xac\xc0wVw|\xa8\xf4\x8dxG\xb7Og\x8b\x8au?\x8c\xe3(\x0c\xec+\x0c\xc3\x8a\xe8k\x8f\x00\xc1\xf8\x95*\xe5\n\xc8fm\xdd\xcbIB\x97"B\x1d}\xa2m8v\x9a\xcf.:\x9f\xf2\xd9@\x11.\x92\xd0\x1dkHzet\xd7\xe6\xc0j\xab\xad\xff\xb3\xe6$\x97\xfd=\x0b\x1c%_\xd1\xa9"'
m9 = ''#YOUR ANSWER HERE
################

################
e10 = 65537
n10 = 98326993759634789515778687799020543645398962489890436310231025647956456166685176265303236823165224008000474960054742885390051491705558213022700710136581245927093740780985394183390749017153700221212481058983678953171251665248666951370742484457781880038452217032906924859256620548427923611534146579043548158531
cipher10 = '?+\xdfn\x17R\xfc;\x84\xcc<)\xceC\xad\x12y\xaa\x85#\xf1G\xd0\x1fF\xd1F\xc4\xdb\x00\xd0\x8c\xc7\xc1\xa0\xc6}P\xd3\xf0\nHB\xdb\x1b\xd3A\xab8\x0f\xcf\xc6\xe9N\x01\x03\x96\n\xb7\x1bU[\xd3\xf2\xe1z\xe2Y\xb0bH\x0f\xd1\x12\x80\xe3\xb7\x1b\x1aU\xd8\xf3\x8c\xcc\xa1\xad\x8dK\xc8\xba\xc4\xcd\x18j"A\xb6\x1b\xd0\xc4\xd5\x9aVT]biR\xb0\xa8p\xc1U$\t\x97\xfe\r(\x95\xc5V\xff]#\xa2\xe3\xf6'
m10 = ''#YOUR ANSWER HERE
################

################
e11 = 65537
n11 = 59271838373237712241010698426785545947980750376894660532845611609385295493574642459966039842508102834600550821189433548722152899983884277266737416092985257305168009937861700509240511070647418413603755912503843488856979904991517729100725512850421664634705274281314737938901139871448406073842088742598680079967
cipher11 = 'J\xc1R\x90\xe1\xf4\x8b5My\xf8\xa1\xf4>\xa2\xc3\x10\xbd\xeb\xcc&\x7fb\x1aC$\x1d\xc5\xb7\xcdz\xb7\x17\x8a#9\x12\x89\xfeao\x19\x9c\xeb\xb0>\x86\x9b\x1d3~b0-u\xfc\x04!\rc\\\xcb$\x91\x9e\xa1N\x9d2\xff\x19\x9a9vH.\xd5\xe7m\xa9m\xea^\xd3T$\xd7\xd7\x11\x81\xe4B\x9b~\x8c $\xa6K\x8a\xdc`\xb4\x9cu\xfb\xc2\x06\xd1\xbb\xb9\xa0\x8f\xd2\xbc\x02\xf6#\x1f\x1dM\xbb\x98\xf2\xa0\x9fO\x80'
m11 = ''#YOUR ANSWER HERE
################

################
e12 = 65537
n12 = 72216220929585874029800250341144628594049328751082632793975238142970345801958594008321557697614607890492208014384711434076624375034575206659803348837757112962991028175041084288364853207245546083862713417245642824765387577331828704441227356582723560291425753389466410790421096831823015438162111864463275922441
cipher12 = ".\xfd9\x8dc\xda\xf9o\xf5Vl\xfb\x87\xed\xd5 \xee\xcf\x97~\xd8T\xf9.\x18\xb1\xd5n^\xa0\rA\xe0\x1d\xd5\xc8:D\xc9\x14o\xde\xdbo\xf9>)bc'a\xa2\x8e\xc1|\xdd\r[q1\xac\x0f^\x82b/A\x10\x87\xff\xe4k=\xc8\xd6\x1c\x7f\xfb\xdb\xda&\xd9\xc5\xc4\x8a#\xa0u\x03J&\n\x83\xa0\xe1.\xba\xfd\x8a0s?\xdeg\xd50\x15\xeb\x91\xb3E\xc7\x15O\xf3r\xe3`~8\xb4\xb5=\x89U\x7f\xfa\x19"
m12 = ''#YOUR ANSWER HERE
################

################
e13 = 3
n13 = 70312356315714780126407430932110548424144037560501611854827137092512910875581601526352040261858471208166388560443445258525272960150598064892138505585965821412085549228607722662540954787033730390722435251172318708904239583536234789288179180688257614871029465697421428231000338910272301520713624044424711448629
cipher13 = '&\xb91\x8ex\x91!0\x855jX\xd1Y\xfc\x9a \xf1\xd9\x9a\xa4\x84s\x0c\xf0\x96\x9e\xcc\xa4L\xe6o\x12\x11~\xd8\xef\x11-t\xf5\xfce\x8a\xb1\xc2mL\xa8\xaa\xb71\xd4y\xa4\xd1\x15\xfdn\x1a\x16\xdf\xfb\xe7\x83Zi\x8f\xb7\x151K\xc72\xf6\xe6\xb31c\xc9\x18\xe9\x92u]\x9f\x01j\x12\xd2\xd3Y("\x9bm9\xc3\x1a9\x1e\xb4\xd4\xa3\xfei\x97\x8a\xa3k\xdc}\xfcy\xf4z\x96\x98\xbev\xce\xa5j\xfdk!xV'
m13 = ''#YOUR ANSWER HERE
################

################
e14 = 65537
n14 = 99428965906962816070784007311850456823957258033424536090292194626620222742187661756726403412281396587119713030320975423136670466362256289782688266974070489861007966741029067535118700826392643025215295741522514598507712664582141077802475427001379922637288480239204598457282788664201418160351588075772782828233
cipher14 = ':\xba\xb7\x0f`\x959\xc2\x900\xf0b\xb3\xe6\xde\xe6\x80\xdf\xc9\x1b\xed\xa6G\x90\x0c\xc2\xa4Z\xc1\x85n\xb6K/\x97\xd4\x9b\x0cKC\x1b\x9e\x83\x13{\x8a\xa6\xa3\x01\xed\x142\xf3\xab\xbb\x1f\x96bQO\x00\x1c\xc5\xba\xfc\xaf\xf2=\x9c\xaa\x94&3aN\r\xe2xh\xad\x18\xf4X\xc1;\xe8\xbcmOn]\xd2JO:+z\xbd\xa6_Q\x10\xf8\xde\xf6`\xdfF\xfa<\xe3 N%$ev\x08\xdai\x85\x8f\x17\xfb,\xa9s\x85'
m14 = ''#YOUR ANSWER HERE
################

################
e15 = 65537
n15 = 118399170574854942444633896245235023966560880236530051363584486215325592633889564680653306117442159965072738319247448982717567259059972729844114596818478915558131833772330699563816353891596654144981880987927436049203299944850160662951894970183034856877612682945727163824998131146307156333199771146520933436033
cipher15 = '@\xc4X\x1a\xae\xb6C\x12.\xfcvK\x90s\xbe\xf2\xab\xda#j\xba\xf7\x81\xee\xa2\xb2\xddR~Z\xbak(u\xee\x90\xf9\xbc\xe3m\xc8\xdb\xf37k\xe8\xb0\xac\xc2T\xe9\x97\xe4\x01~\xdd\xd4A\xd3\xe9\\\x876}#\xddK7n\xae\x1e\xed\xe6z\x82Zp\xe5c\xc0C\xbd\xf9\x8bD\x03\x19\x9d\xb5s \x0f\xe1c\xd4\xf5M\xc4\xbc\x971\x87\xd6\xb5\x1d\x10\xb7\xc4/\xf6\x8d!u\xed\xe9|U\xbe\x98\xbaLLp\x8ehZ\xec\x1d'
m15 = ''#YOUR ANSWER HERE
################

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

def hex_to_string(h):
    return bits_to_string(hexs_to_bits(h))

def xor(p, q):
    if len(p)!=len(q):
        print p, q
        raise AssertionError
    k = [0]*len(p)
    for i in range(len(p)):
        k[i] = (int(p[i])+int(q[i])) % 2
    return "".join([str(m) for m in k])

def xor1(a, b):
    assert len(a) == len(b)
    return [aa^bb for aa, bb in zip(a, b)]

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
    #print p
    #print q
    assert gmpy.is_prime(p)
    assert gmpy.is_prime(q)
    assert p*q==N
    return p, q

#print find1(N1)

def find2(N):
    A = B = gmpy.mpz(gmpy.sqrt(N)+1)
    while True:
        try:
            return find1(N, A)
        except:
            A = A+1
            if A - B > 2**20:
                return False
            pass

#print find2(N2)

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
        return p1, q1
    elif gmpy.is_prime(p2) and gmpy.is_prime(q2) and p2*q2==N:
        return p2, q2
    else:
        assert False
        
def find4(N):
    A = B = gmpy.mpz(gmpy.sqrt(24*N)+1)
    while True:
        try:
            return find3(N, A)
        except:
            A = A+1
            if A - B > 2**20:
                return False
            pass

#find3(N3)
#find4(N3)

c = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

def rsa(c, n, e, p, q=None):
    if q == None:
        q = n/p
        assert gmpy.is_prime(p) and gmpy.is_prime(q)
    f = n - p - q + 1
    g, d, y = xgcd(e, f)
    if d <= 0:
        d = d+f
    print g, d*e % f
    pt = powmod(c, d, n)
    bpt = convert_to_bits(pt, 1024)
    hpt = bits_to_hex(bpt)
    #print hpt
    #print len(hex(pt))
    return pt, ''.join([str(i) for i in bpt])

p, q = find1(N1)
#rsa(c, N1, 65537, p, q)

tar_pt = int(0x466163746f72696e67206c65747320757320627265616b205253412e)
#print hex(tar_pt)
print bits_to_string(convert_to_bits(tar_pt, 28*8))

n = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15]
e = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]
c = [cipher0, cipher1, cipher2, cipher3, cipher4, cipher5, cipher6, cipher7, cipher8, cipher9, cipher10, cipher11, cipher12, cipher13, cipher14, cipher15]

c_int = [0 for i in range(len(c))]
for i in range(len(c)):
    k = c[i]
    c_b = string_to_bits(k)
    c_i = bits_to_int(c_b)
    c_int[i] = c_i

def brute_find(i, t = 20):
    j = 0
    n_i = n[i]
    c_i = c_int[i]
    e_i = e[i]
    while j < 2**t:
        k, t = gmpy.root(n_i*j+c_i, e_i)
        if t == 1:
            print k
            return k
        j += 1
    pass

def hash(input_, length):
    h = sha512(bits_to_string(input_)).digest()
    return [int(i) for i in string_to_bits(h)[:length]]

def brute_find2(i, t = 20):
    j = 0
    n_i = n[i]
    c_i = c_int[i]
    e_i = e[i]
    for i in range(2**t):
        j = gmpy.next_prime(j)
        g, d, y = xgcd(j, n_i)
        if g != 1:
            print j
            return j
    pass

def decrypt(num, g=512, h=512):
    pt = convert_to_bits(num, 1024)
    G = pt[:g]
    H = pt[g:]
    print len(pt), len(H)
    nonce = xor1(H, hash(G, h))
    mm = xor1(G, hash(nonce, g))
    return mm

def crt(a, m):
    M = 1
    for i in m:
        M *= i
        b = [gmpy.invert(M / m[i], m[i]) for i in range(len(m))]
        x = 0
    for i in range(len(m)):
        x += a[i] * b[i] * M / m[i]
    return x

m_i1 = 423125987157051944371127445820542159149056283811701171840365
m_i9 = 4918655522832920298361237301768640132854372891951182963303463195494000723811010749317062690711647121471
###print brute_find(1)
##print brute_find(2)
##print brute_find(8)
###print brute_find(9)
##print brute_find(13)
##
##print brute_find(3)
##print brute_find(4)
##print brute_find(5)
##print brute_find(6)
##print brute_find(7)
##print brute_find(10)
##print brute_find(11)
##print brute_find(12)
##print brute_find(14)
##print brute_find(15)

p0, q0 = find2(n0)
p6, q6 = find2(n6)
p11 = 7924057187763558064452801291482013694582305119032293927979457583171139106404218548653442118775641945544367293470393031489286439304696105851789091398057521
p12 = 7924057187763558064452801291482013694582305119032293927979457583171139106404218548653442118775641945544367293470393031489286439304696105851789091398057521

##print p0, q0
##print p6, q6
##
##print 'case 0'
##m_i0, m_b0 =  rsa(c_int[0], n[0], e[0], p0)
##print 'case 6'
##m_i6, m_b6 = rsa(c_int[6], n[6], e[6], p6)
##print 'case 11'
##m_i11, m_b12 = rsa(c_int[11], n[11], e[11], p11)
##print 'case 12'
##m_i12, m_b11 = rsa(c_int[12], n[12], e[12], p12)

def int_to_string(i, n=1040):
    b = convert_to_bits(i, n)
    b = ''.join(str(j) for j in b)
    s = bits_to_string(b)
    return s
    
##print 'case 0'
##print int_to_string(m_i0)
##print 'case 1'
##print int_to_string(m_i1)
##print 'case 6'
##print int_to_string(m_i6)
##print 'case 9'
##print int_to_string(m_i9)
##print 'case 11'
##print int_to_string(m_i11)
##print 'case 12'
##print int_to_string(m_i12)

##e = 65537
##n = 132177882185373774813945506243321607011510930684897434818595314234725602493934515403833460241072842788085178405842019124354553719616350676051289956113618487539608319422698056216887276531560386229271076862408823338669795520077783060068491144890490733649000321192437210365603856143989888494731654785043992278251
##
##################
### Here are two example signatures
###
### First message
##m1 = 387
### first signature
##s1 = 104694095966994423550399840405679271451689287439740118881968798612714798360187905616965324945306116261186514828745033919423253353071142760352995900515279740753864505327750319034602409274084867637277266750899735986681083836544151016817569622466120342654469777762743360212628271549581658814852850038900877029382
##
### Second message
##m2 = 2
### second signature
##s2 = 18269259493999292542402899855086766469838750310113238685472900147571691729574239379292239589580462883199555239659513821547589498977376834615709314449943085101697266417531578751311966354219681199183298006299399765358783274424349074040973733214578342738572625956971005052398172213596798751992841512724116639637

crt_a = [c_int[2], c_int[8], c_int[13]]
crt_m = [n2, n8, n13]
k = crt(crt_a, crt_m)
k = k % (n2*n8*n13)
##for i in range(2**20):
##    w = k+i*n2*n8*n13
##    r, t = gmpy.root(w, 3)
##    if t:
##        print r
        
r = 115330225273195376368258849833825724706744238235173445386760843688436021905519659519862304119012652370067213152781258007253397635626260859138670066646774241596749797148417081756331607660340407490653896244676830309998789071180670033580950438360343921637483889543124019468107336998983044592605773812924869352747
decrypt(r)

##for i in range(2**20):
##    w = k+i*n2*n8*n13
##    r, t = gmpy.root(w, 3)
##    if t:
##        print r

def brute_find3(i, t = 15, precise = True):
    n_i = n[i]
    c_i = c_int[i]
    e_i = e[i]
    for i in range(t**2):
        if precise:
            p, q, n_pq = what(i)
            if n_pq == n_i:
                print p, q
                return p, q
        else:
            p, q, n_pq = what(i)
            g, d, y = xgcd(p, n_i)
            if g != 1:
                print p
                return j
            g, d, y = xgcd(q, n_i)
            if g != 1:
                print q
                return j
    pass
    
n_f = 123139257250126329072773726675243257580550728065510250355050105040961069379571235556595226046554214827510742496799970195881106280437959158707238296876219608776490854355708792879135769996451404921631130134104207090055751549504641860375460355336235614906774988828468421536178729380641488939620270782145238346367

e_f =  65537

c_f = 57965430336257636084035573816581975071479949225554750322490082458883367138745850378055599493856871005253443127798571076614963471843544300372785467082456903912582920032952075898375680087224118457537839632906323084782810030136022267386317308489651192392430531335489752213468975310380802367312825891307058273972

def d_final():
    for i in range(100):
        if powmod(i, e_f, n_f)==c_f:
            return i

#d_final() == 87

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
