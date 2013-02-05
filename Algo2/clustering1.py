kc = 4
n = 500

edges = open("clustering1.txt")
line = edges.readline()
line = line.split()
graph = []
line = edges.readline()
while line:
    w = [int(i) for i in line.split()]
    graph.append([w[-1]] + w[0:-1])
    line = edges.readline()

print len(graph)
print min([w[1] for w in graph]+[w[2] for w in graph])
print max([w[1] for w in graph]+[w[2] for w in graph])

graph.sort()

##kc = 2
##n = 4
##graph = [[10,1,2], [20,2,3], [15,3,4], [18,1,3],[30,1,4],[50,2,4] ]
##graph.sort()

k = [(i, i) for i in range(1, n+1)]
n2c = dict(k)
k = [(i, [i]) for i in range(1, n+1)]
c2n = dict(k)
cost = 0
while True:
    a = graph.pop(0)
    assert a[0] >= cost
    cost = a[0]
    if n2c[a[1]] == n2c[a[2]]:
        continue
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
    if len(c2n) < kc:
        break
    

print cost
