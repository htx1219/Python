import math
import numpy

graph = open("tsp.txt")
line = graph.readline()
node = int(line)
line = graph.readline()
tsp_map = []
while line:
    a = line.split()
    tsp_map.append(numpy.array([float(a[0]), float(a[1])]))
    line = graph.readline()

print len(tsp_map), node

def d(tsp_map, i, j):
    return numpy.linalg.norm(tsp_map[i] - tsp_map[j])

w = 2**(node-1)
A = numpy.ones((node, w))
