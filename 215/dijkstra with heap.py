def up_heapify(L, i, k):
    if i == 0:
        return
    p = parent(i)
    if L[p] > L[i]:
        L[i], L[p] = L[p], L[i]
        k[L[p][1]], k[L[i][1]] = k[L[i][1]], k[L[p][1]]
        return up_heapify(L, p, k)
    return i

def remove_min(L, k):
    L[0], L[-1] = L[-1], L[0]
    k[L[0][1]], k[L[-1][1]] = k[L[-1][1]], k[L[0][1]]
    del k[L[-1][1]]
    L.remove(L[-1])    
    down_heapify(L, 0, k)
    return

def parent(i): 
    return (i-1)/2
def left_child(i): 
    return 2*i+1
def right_child(i): 
    return 2*i+2
def is_leaf(L,i): 
    return (left_child(i) >= len(L)) and (right_child(i) >= len(L))
def one_child(L,i): 
    return (left_child(i) < len(L)) and (right_child(i) >= len(L))

def down_heapify(L, i, k):
    # If i is a leaf, heap property holds
    if is_leaf(L, i): 
        return
    # If i has one child...
    if one_child(L, i):
        # check heap property
        if L[i] > L[left_child(i)]:
            # If it fails, swap, fixing i and its child (a leaf)
            (L[i], L[left_child(i)]) = (L[left_child(i)], L[i])
            k[L[left_child(i)][1]], k[L[i][1]] = k[L[i][1]], k[L[left_child(i)][1]]
        return
    # If i has two children...
    # check heap property
    if min(L[left_child(i)], L[right_child(i)]) >= L[i]: 
        return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if L[left_child(i)] < L[right_child(i)]:
        # Swap into left child
        (L[i], L[left_child(i)]) = (L[left_child(i)], L[i])
        k[L[left_child(i)][1]], k[L[i][1]] = k[L[i][1]], k[L[left_child(i)][1]]
        down_heapify(L, left_child(i), k)
        return
    else:
        (L[i], L[right_child(i)]) = (L[right_child(i)], L[i])
        k[L[right_child(i)][1]], k[L[i][1]] = k[L[i][1]], k[L[right_child(i)][1]]
        down_heapify(L, right_child(i), k)
        return

def build_heap(L):
    for i in range(len(L)-1, -1, -1):
        down_heapify(L, i)
    return L

def search_list(L, v):
    for i, k in enumerate(L):
        if k[1] == v:
            return i, k[0]

def dijkstra(G,v):
    dist_so_far = []
    d_dist = {}
    dist_so_far.append((0, v))
    d_dist[v] = 0
    final_dist = {}
    while len(final_dist) < len(G):
        ww = dist_so_far[0]
        # lock it down!
        w = ww[1]
        final_dist[w] = ww[0]
        remove_min(dist_so_far, d_dist)
        for x in G[w]:
            if x not in final_dist:
                if x not in d_dist:
                    k = final_dist[w] + G[w][x]
                    dist_so_far.append((k, x))
                    d_dist[x] = len(dist_so_far)-1
                    up_heapify(dist_so_far, len(dist_so_far)-1, d_dist)
                elif final_dist[w] + G[w][x] < dist_so_far[d_dist[x]][0]:
                    k = final_dist[w] + G[w][x]
                    n = d_dist[x]
                    dist_so_far[n] = (k, x)
                    up_heapify(dist_so_far, len(dist_so_far)-1, d_dist)
    return final_dist

import heapq

def dijkstra(G,v):
    dist_so_far = []
    distMap = {v: 0}
    heapq.heappush(dist_so_far, (0, v))
    final_dist = {}
    while len(final_dist) < len(G):
        d, w = heapq.heappop(dist_so_far)
        while d != distMap[w]:
          d, w = heapq.heappop(dist_so_far)
        # lock it down!
        final_dist[w] = d
        for x in G[w]:
            if x not in final_dist:
              d = final_dist[w] + G[w][x]
              if x not in distMap or d < distMap[x]:
                distMap[x] = d
                heapq.heappush(dist_so_far, (d, x))
    return final_dist

############
# 
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra(G, a)
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)
    print "test pass"
   
test()
