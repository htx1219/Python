def bipartite(G):
    to_check = [G.keys()[0]]
    set1 = []
    set2 = []
    while to_check:
        k = to_check.pop(0)
        if not set1:
            set1.append(k)
            set2 = set2 + G[k].keys()
            to_check = to_check + G[k].keys()
        elif k in set1:
            for w in G[k]:
                if w not in set2:
                    set2.append(w)
                    to_check.append(w)
        elif k in set2:
            for w in G[k]:
                if w not in set1:
                    set1.append(w)
                    to_check.append(w)
    for p in set2:
        for k in G[p]:
            if k in set2:
                return None
    for p in set1:
        for k in G[p]:
            if k in set1:
                return None
    return set(set1)


########
#
# Test

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G


def test():
    edges = [(1, 2), (2, 3), (1, 4), (2, 5),
             (3, 8), (5, 6)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert (g1 == set([1, 3, 5]) or
            g1 == set([2, 4, 6, 8]))
    edges = [(1, 2), (1, 3), (2, 3)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert g1 == None

test()
