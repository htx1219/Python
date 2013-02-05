import random

text = open("2sat2.txt")
line = text.readline()
varnum = int(line)
line = text.readline()
clauses = []
while line:
    a = line.split()
    clauses.append((int(a[0]), int(a[1])))
    line = text.readline()

print len(clauses)

def sign(n):
    return n>0

def solve_2SAT(varnum, clauses):
    for sth in range(0,4):
        x = [-1]*(varnum/2) +[1]*(varnum/2)
        random.shuffle(x)
        print "finish initialization for # of pass:", sth
        for sth2 in range(1, 3*varnum):
            if sth2 % 10000 == 0:
                print sth2
            sat = True
            n = random.randint(0, varnum-1)
            for i in range(0, varnum):
                clause = clauses[(i+n) % varnum]
                if (sign(x[abs(clause[0])-1]) != sign(clause[0])) and (sign(x[abs(clause[1])-1]) != sign(clause[1])):
                    sat = False
                    break
            if sat:
                print "satisfied!"
                return
            k = random.randint(0,1)
            x[abs(clause[k])-1] = -x[abs(clause[k])-1]
    print "All complete, not satified"
    return None
            
solve_2SAT(varnum, clauses)
