edges = open("edges.txt")
line = edges.readline()
line = line.split()
graph = []
line = edges.readline()
while line:
    graph.append([int(i) for i in line.split()])
    line = edges.readline()

print len(graph)
print min([w[0] for w in graph]+[w[1] for w in graph])
print max([w[0] for w in graph]+[w[1] for w in graph])

nodes = {1:True}
tree = []
while len(nodes) < 500:
    min_cost = None
    min_edge = None
    for edge in graph:
        if min_cost == None:
            min_cost = edge[2]
            min_edge = edge[:]
        if ((edge[0] in nodes and edge[1] not in nodes) or (edge[0] not in nodes and edge[1] in nodes)) and edge[2] < min_cost:
            min_cost = edge[2]
            min_edge = edge[:]
    tree.append(min_edge)
    if min_edge[0] in nodes and min_edge[1] not in nodes:
        nodes[min_edge[1]] = True
    elif min_edge[1] in nodes and min_edge[0] not in nodes:
        nodes[min_edge[0]] = True
    else:
        raise NodeError

print len(nodes)
print len(tree)
print sum([e[2] for e in tree])
    
            
        
        
        
