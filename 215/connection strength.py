import csv

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    for (node1, node2) in tsv: make_link(G, (node1, 'Star'), (node2, 'Book'))
    return G

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    try:
        (G[node1])[node2] += 1
    except:
        G[node1][node2] = 1
    if node2 not in G:
        G[node2] = {}
    try:
        (G[node2])[node1] += 1
    except:
        G[node2][node1] = 1
    return G

def make_second_graph(G):
    G2 = {}
    for k in G:
        if k[1] == 'Star':
            for k2 in G[k]:
                if k2[1] == 'Book':
                    for k3 in G[k2]:
                        if k3[1] == 'Star' and k3 != k:
                            make_link(G2, k[0], k3[0])
    return G2

def most_link(G):
    max_w = 0
    max_pair = (None, None)
    for k in G:
        for k2 in G[k]:
            if G[k][k2] > max_w:
                max_w = G[k][k2]
                max_pair = (k, k2)
    return max_w, max_pair

k = read_graph('Marvel.txt')
k2 = make_second_graph(k)
#print most_link(k2)

import heapq

k3 = {}
for node in k2:
    for node2 in k2[node]:
        if node in k3:
            k3[node][node2] = 1.0/k2[node][node2]
        else:
            k3[node] = {}
            k3[node][node2] = 1.0/k2[node][node2]

k4 = {}
for node in k2:
    for node2 in k2[node]:
        if node in k4:
            k4[node][node2] = 1
        else:
            k4[node] = {}
            k4[node][node2] = 1

def dijkstra(G,v):
    dist_so_far = []
    distMap = {v: 0}
    heapq.heappush(dist_so_far, (0, v, 0))
    final_dist = {}
    while len(final_dist) < len(G):
        if not dist_so_far:
            break
        d, w, l = heapq.heappop(dist_so_far)
        while d != distMap[w]:
          d, w, l = heapq.heappop(dist_so_far)
        # lock it down!
        final_dist[w] = (d, l)
        for x in G[w]:
            if x not in final_dist:
              d = final_dist[w][0] + G[w][x]
              if x not in distMap or d < distMap[x]:
                distMap[x] = d
                heapq.heappush(dist_so_far, (d, x, l+1))
    return final_dist

l = ['SPIDER-MAN/PETER PAR',
'GREEN GOBLIN/NORMAN ',
'WOLVERINE/LOGAN ',
'PROFESSOR X/CHARLES ',
'CAPTAIN AMERICA']

#test:
d1 = dijkstra(k3, l[0])
d2 = dijkstra(k4, l[0])
print d1['YAP']
print d2['YAP']

d1 = dijkstra(k3, l[2])
d2 = dijkstra(k4, l[2])
print d1['HOARFROST/']
print d2['HOARFROST/']

res = 0
for node in l:
    d1 = dijkstra(k3, node)
    d2 = dijkstra(k4, node)
    for node2 in d1:
        if d1[node2][1] != d2[node2][1]:
            res += 1

print res
