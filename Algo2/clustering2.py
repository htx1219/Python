import itertools

k = 2
b = 24
n = 20000

edges = open("clustering2.txt")
line = edges.readline()
line = line.split()
points = {}
p2 = []
line = edges.readline()
m = 0
while line:
    w = "".join(line.split())
    if w not in points:
        m += 1
    points[w] = m
    p2.append([m, [int(i) for i in line.split()]])
    line = edges.readline()

print len(points)
print len(p2)
print m

x = p2[0][1]
for p in p2:
    r = sum([p[1][i] != x[i] for i in range(0,b)])
    if r <= 2:
        print "newpoint", p[0], x, p[1]

def rev(b):
    if b =='1':
        return '0'
    elif b == '0':
        return '1'
    

nodes = {}
for w in points:
    nodes[points[w]] = []
    for i in range(1, k+1):
        j = itertools.combinations(range(0,b), i)
        for p in j:
            new_w = w
            for q in p:
                new_w = new_w[:q] + rev(new_w[q]) + new_w[q+1:]
            if new_w in points:
                nodes[points[w]].append(points[new_w])

n2c = dict([(i, i) for i in range(1, m+1)])
c2n = dict([(i, [i]) for i in range(1, m+1)])
for w in nodes:
    if len(nodes[w]) > 0:
        for q in nodes[w]:
            if n2c[q] == n2c[w]:
                continue
            a = [True, q,w]
            if len(c2n[n2c[a[1]]]) >= len(c2n[n2c[a[2]]]):
                p = c2n.pop(n2c[a[2]])
                c2n[n2c[a[1]]] += p
                c = n2c[a[1]]
                for n in p:
                    n2c[n] = c
            else:
                p = c2n.pop(n2c[a[1]])
                c2n[n2c[a[2]]] += p
                c = n2c[a[2]]
                for n in p:
                    n2c[n] = c

print len(c2n)
