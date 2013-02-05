from copy import deepcopy
from math import log
from random import randrange

nums = open("MinCut.txt")
graph = []
line = nums.readline()
while line:
    nodes = line.split()
    graph.append((nodes[0],nodes[1:]))
    line = nums.readline()
print len(graph)

toygraph = [("1",["2","3","4"]),
            ("2",["1","3","4","5"]),
            ("3",["1","2","4"]),
            ("4",["1","2","3","7"]),
            ("5",["2","6","7","8"]),
            ("6",["5","7","8"]),
            ("7",["4","5","6","8"]),
            ("8",["5","6","7"])]

def mincut(graph, res = False):
    l = len(graph)
    short = num_edge(graph)
    short_g = graph
    for i in range(int(l*l*log(l))):
        if i%100 == 0:
            print i, " times iteration, shortest cut is ", short
        graph1 = deepcopy(graph)
        cut, g = all_confus(graph1)
        if cut < short:
            short = cut
            short_g = g
    if res == True:
        print short_g
    return short
        
def num_edge(graph):
    num = 0
    for k in graph:
        num += len(k[1])
    assert num %2 == 0
    return num/2

def x_edge(graph, x):
    for k in graph:
        if x < len(k[1]):
            return (k[0], k[1][x])
        else:
            x -= len(k[1])

def all_confus(graph):
    while len(graph) > 2:
        confusion(graph)
    return num_edge(graph), graph

def graph_find(graph, node):
    for k in graph:
        if k[0] == node:
            return k[1]

toygraph1 = deepcopy(toygraph)
def confusion(graph):
    x = randrange(0, num_edge(graph))
    edge = x_edge(graph, x)
    edge_head = graph_find(graph, edge[1])
    edge_tail = graph_find(graph, edge[0])
    new_edge = edge_head+edge_tail
    while edge[0] in new_edge:
        new_edge.remove(edge[0])
    while edge[1] in new_edge:
        new_edge.remove(edge[1])
    graph.remove((edge[1], edge_head))
    graph.remove((edge[0], edge_tail))
    new_node = edge[0]+"+"+edge[1]
    for k in graph:
        while edge[0] in k[1]:
            k[1].remove(edge[0])
            k[1].append(new_node)
        while edge[1] in k[1]:
            k[1].remove(edge[1])
            k[1].append(new_node)
    graph.append((new_node, new_edge))
    return graph
    
    

            
    
