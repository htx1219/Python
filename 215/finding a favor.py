from heap import *
from operator import itemgetter
import heapq
from math import log, exp

def maximize_probability_of_favor(G, v, v2):
    try:
        nodes = len(G)
        edges = sum([len(G[k]) for k in G.keys()])
        #print nodes, edges
        H = {}
        for k in G:
            H.setdefault(k, {})
            for k2 in G[k]:
                try:
                    H[k][k2] = -log(G[k][k2])
                except:
                    pass
        try:
            if nodes**2 < edges*log(nodes):
                final_dist = dijkstra_list(H, v)
            else:
                final_dist = dijkstra_heap(H, v)
        except:
            return None, 0
        #print final_dist
        if v2 not in final_dist:
            return None, 0
        node = v2
        path = []
        while node:
            path = [node] + path
            now = final_dist[node]
            if node == v:
                break
            node = now[1]
        if path[0] == v:
            return path, exp(-final_dist[v2][0])
        return None, 0
    except:
        return None, 0

def bfs(G, v1, v2):
    """
    returns true if path from v1 to v2 exists, else - false
    """
    if v1==v2:
        return True
    tested = set([v1])
    q = [v1]
    while q:
        cur = q.pop(0)
        for neighbor in G[cur]:
            if neighbor not in tested:
                tested.add(neighbor)
                q.append(neighbor)
            if neighbor == v2:
                return True
    return False

def maximize_probability_of_favor(G, v1, v2):
    """
    # your code here
    # call either the heap or list version of dijkstra
    # and return the path from `v1` to `v2`
    # along with the probability that v1 will do a favor
    # for v2
    """
    if v1==v2:  ## itself - probability 1
        return ([v1], 1.0)

    if not bfs(G,v1,v2):  ## no path - probability 0
        return (None,0.0)
    n = len(G)  #number of vertex
    m = sum([len(G[node]) for node in G])  #number of edges
    inf = 9999999999999
    logG = {} ### change original values of G to its minus logarithm
    for ver1 in G:
        logG[ver1] = {}
        for ver2 in G[ver1]:
            if G[ver1][ver2]!=0:
                logG[ver1][ver2] = - log(G[ver1][ver2])
            else:
                logG[ver1][ver2] = inf

    dijkstra = dijkstra_heap if m*log(n) <  n**2 else dijkstra_list ##choose function

    d = dijkstra(logG, v1)
    (logProb, par) = d[v2]
    path = [par, v2]
    while par!=v1:
        (tmp, par) = d[par]  ##backtracking path finding
        path.insert(0, par)

    return (path, exp(-logProb))

def maximize_probability_of_favor2(G, v, v2):
    nodes = len(G)
    edges = sum([len(G[k]) for k in G.keys()])
    if True: #nodes**2 < 10*edges:
        return dij_list(G, v, v2)
    else:
        return dij_heap(G, v, v2)

def dij_list(G, v, v2):
    dist_so_far = {v: (1, [v])}
    final_dist = {}
    while len(final_dist) < len(G):
        if dist_so_far:
            w, (p, path) = max(dist_so_far.items(), key = itemgetter(1))
            del dist_so_far[w]
        else:
            break
        # lock it down!
        final_dist[w] = (p, path)
        for x in G[w]:
            if x not in final_dist:
                p = final_dist[w][0]*G[w][x]
                path = final_dist[w][1] + [x]
                if x not in dist_so_far or p > dist_so_far[x][0]:
                    dist_so_far[x] = (p, path)
    if v2 in final_dist:
        return (final_dist[v2][1], final_dist[v2][0])
    else:
        return (None, 0)

def dij_heap(G, v, v2):
    dist_so_far = []
    distMap = {v: (-1, [v])}
    heapq.heappush(dist_so_far, (-1, v, [v]))
    final_dist = {}
    while len(final_dist) < len(G):
        if dist_so_far:
            p, w, path = heapq.heappop(dist_so_far)
        else:
            break
        while p != distMap[w][0]:
            if dist_so_far:
                p, w, path = heapq.heappop(dist_so_far)
            else:
                break
        # lock it down!
        final_dist[w] = (p, path)
        for x in G[w]:
            if x not in final_dist:
              p = final_dist[w][0]*G[w][x]
              path = final_dist[w][1] + [x]
              if x not in distMap or p < distMap[x][0]:
                distMap[x] = (p, path)
                heapq.heappush(dist_so_far, (p, x, path))
    if v2 in final_dist:
        return (final_dist[v2][1], -final_dist[v2][0])
    else:
        return (None, 0)

def dijkstra_heap(G, a):
    # Distance to the input node is zero, and it has
    # no parent
    first_entry = (0, a, None)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry:0}
    dist_so_far = {a:first_entry} 
    final_dist = {}
    while len(dist_so_far) > 0:
        dist, node, parent = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = (dist, parent)
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, x, node)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_dist < dist_so_far[x]:
                # update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist

#
# version of dijkstra implemented using a list
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_list(G, a):
    dist_so_far = {a:(0, None)} #keep track of the parent node
    final_dist = {}
    while len(final_dist) < len(G):
        node, entry = min(dist_so_far.items(), key=itemgetter(1))
        # lock it down!
        final_dist[node] = entry
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, node)
            if x not in dist_so_far:
                dist_so_far[x] = new_entry
            elif new_dist < dist_so_far[x]:
                dist_so_far[x] = new_entry
    return final_dist

N = {1: {2: 31.77885962789011, 3: 3.8643869266344852},
 2: {1: 6.928039917634328},
 3: {2: 1.625029450403147},
 4: {1: 2.3721444740936932, 2: 5.221635415114583}}
    
def test():
    G = {'a':{'b':.9, 'e':.5},
         'b':{'c':.5},
         'c':{'d':.01},
         'd':{},
         'e':{'f':.5},
         'f':{'d':.5}}
    path, prob = maximize_probability_of_favor(G, 'a', 'd')
    print path, prob
    assert path == ['a', 'e', 'f', 'd']
    assert abs(prob - .5 * .5 * .5) < 0.001
    assert maximize_probability_of_favor(G, 'a', 'f') == (['a', 'e', 'f'], 0.25)
    assert maximize_probability_of_favor(G, 'a', 'a') == (['a'], 1.0)
    assert maximize_probability_of_favor(G, 'd', 'a') == (None, 0)
    assert maximize_probability_of_favor(G, 'c', 'f') == (None, 0)

    print 'test pass'

test()
