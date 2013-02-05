def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = w
    (G[node1])[node2] = w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = w
    (G[node2])[node1] = w
    return G

def create_weighted_graph(bipartiteG, characters):
    G = {}
    leng = len(bipartiteG.keys())-len(characters)
    for k in characters:
        for k1 in characters:
            if k != k1:
                p1 = set(bipartiteG[k].keys())
                p2 = set(bipartiteG[k1].keys())
                inter = p1&p2
                if len(inter):
                    make_link(G, k, k1, len(inter)*1.0/leng)         
    return G



def create_weighted_graph2(bipartiteG, characters):
    G = {}
    leng = len(bipartiteG.keys())-len(characters)
    for k in bipartiteG:
        if k not in characters:
            for k2 in bipartiteG[k]:
                for k3 in bipartiteG[k]:
                    if k2 != k3:
                        G.setdefault(k2, {})
                        G[k2].setdefault(k3, 0)
                        G[k2][k3] += 1.0/leng
    return G

######
#
# Test

def test():
    bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                  'charB':{'comicB':1, 'comicC':1, 'comicD':1},
                  'charC':{'comicD':1},
                  'comicB':{'charA':1, 'charB':1},
                  'comicC':{'charA':1, 'charB':1},
                  'comicD': {'charC':1, 'charB':1}}
    G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
    print G
    # three comics contain charA or charB
    # charA and charB are together in one of them
    assert G['charA']['charB'] == 1.0 / 3
    assert G['charA'].get('charA') == None
    assert G['charA'].get('charC') == None

test()
