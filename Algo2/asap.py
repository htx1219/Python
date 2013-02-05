graph_t = open("g2.txt")
line = graph_t.readline()
nodes = int(line.split()[0])+1
line = graph_t.readline()
graph = {}
while line:
    a = line.split()
    graph[(int(a[0]), int(a[1]))] = int(a[2])
    line = graph_t.readline()

print len(graph)

#Base Case:
A1 = [[1e10 for i in range(0, nodes)] for j in range(0, nodes)]
A2 = [[1e10 for i in range(0, nodes)] for j in range(0, nodes)]

for i in range(1, nodes):
    A1[i][i] = 0
    for j in range(1, nodes):
        if (i, j) in graph:
            A1[i][j] = graph[(i,j)]
            #if graph[(i, j)] < 0:
#                print i, j, graph[(i, j)]

print "Base Case Complete"

for k in range(1, nodes):
    if k%10 == 0:
        print k
    if k%2 == 1:
        for i in range(1, nodes):
            for j in range(1, nodes):
                A2[i][j] = min(A1[i][j], A1[i][k]+A1[k][j])
    else:
        for i in range(1, nodes):
            for j in range(1, nodes):
                A1[i][j] = min(A2[i][j], A2[i][k]+A2[k][j])

print "All Case Complete"

for i in range(1, nodes):
    if A1[i][i] < 0:
        print "Contain negative cycle"
        break

print "Check for the shortest path"

short = 0
for i in range(1, nodes):
    for j in range(1, nodes):
        if A1[i][j] < short:
            short = A1[i][j]
print short
