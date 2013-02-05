# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1}, 
#      'b': {'a': 1, 'd': 1}, 
#      'c': {'a': 1, 'd': 1}, 
#      'd': {'c': 1, 'b': 1, 'e': 1}, 
#      'e': {'d': 1, 'g': 1, 'f': 1}, 
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1} 
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'}, 
#      'b': {'a': 'green', 'd': 'red'}, 
#      'c': {'a': 'green', 'd': 'green'}, 
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'} 
#      }
#

def make_link(G, node1, node2, res = 1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = res
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = res
    return G

def make_link_directed(G, node1, node2, res = 1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = res
    return G

def create_rooted_spanning_tree(G, root):
    S = {}
    l = [root]
    while l:
        r = l.pop(0)
        for k in G[r]:
            if k not in S:
                make_link(S, r, k, 'green')
                l.append(k)
            else:
                if k not in S[r]:
                    make_link(S, r, k, 'red')
    return S

def create_rooted_spanning_tree_directed(G, root):
    S = {}
    l = [root]
    while l:
        r = l.pop(0)
        for k in G[r]:
            if k not in S:
                make_link_directed(S, r, k, 'green')
                l.append(k)
    return S

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces
def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    S = create_rooted_spanning_tree(G, "a")
    #print S
    assert S == {'a': {'c': 'green', 'b': 'green'}, 
                 'b': {'a': 'green', 'd': 'red'}, 
                 'c': {'a': 'green', 'd': 'green'}, 
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'} 
                 }

test_create_rooted_spanning_tree()
###########

def post_order(S, root):
    mark = 1
    d = {}
    marked = [root]
    l = [root]
    while l:
        r = l[0]
        complete = True
        for k in S[r]:
            if k not in marked:
                if S[r][k] == 'green':
                    l = [k] + l
                    marked.append(k)
                    complete = False
        if complete:
            d[r] = mark
            mark += 1
            l.remove(r)
    return d

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces
def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    print po
    assert po == {'a':7, 'b':1, 'c':6, 'd':5, 'e':4, 'f':2, 'g':3}

test_post_order()
##############

def number_of_descendants(S, root):
    d = {}
    marked = [root]
    l = [root]
    while l:
        r = l[0]
        complete = True
        for k in S[r]:
            if k not in marked:
                if S[r][k] == 'green':
                    l = [k] + l
                    marked.append(k)
                    complete = False
        if complete:
            d[r] = 1
            for k in S[r]:
                if S[r][k] == 'green':
                    d[r] += d.get(k, 0)
            l.remove(r)
    return d

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'}, 
          'b': {'a': 'green', 'd': 'red'}, 
          'c': {'a': 'green', 'd': 'green'}, 
          'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
          'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'} 
          }
    nd = number_of_descendants(S, 'a')
    print nd
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}

test_number_of_descendants()
###############

def lowest_post_order(S, root, po):
    d = {}
    marked = [root]
    l = [root]
    while l:
        r = l[0]
        complete = True
        for k in S[r]:
            if k not in marked:
                if S[r][k] == 'green':
                    l = [k] + l
                    marked.append(k)
                    complete = False
        if complete:
            d[r] = po[r]
            for k in S[r]:
                d[r] = min(d.get(k, 'infin'), d[r])
                if S[r][k] == 'red' and k in d:
                    d[k] = min(d.get(r, 0), d[k])
            l.remove(r)
    return d

def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    print l
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}

test_lowest_post_order()
################
def highest_post_order(S, root, po):
    d = {}
    marked = [root]
    l = [root]
    while l:
        r = l[0]
        complete = True
        for k in S[r]:
            if k not in marked:
                if S[r][k] == 'green':
                    l = [k] + l
                    marked.append(k)
                    complete = False
        if complete:
            d[r] = po[r]
            for k in S[r]:
                d[r] = max(d.get(k, 0), d[r])
                if S[r][k] == 'red' and k in d:
                    d[k] = max(d.get(r, 0), d[k])
            l.remove(r)
    return d

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    print h
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}

test_highest_post_order()
#################

def bridge_edges(G, root):
    S = create_rooted_spanning_tree(G, root)
    po = post_order(S, root)
    nd = number_of_descendants(S, root)
    l = lowest_post_order(S, root, po)
    h = highest_post_order(S, root, po)
    S_d = create_rooted_spanning_tree_directed(G, root)
    res = []
    for r in S_d:
        if S_d[r]:
            for k in S_d[r]:
                if S_d[r][k] == 'green':
                    if po[k] >= h[k] and l[k] > (po[k] - nd[k]):
                        print po[k], h[k], l[k], nd[k]
                        res.append((r, k))
    return res

def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    bridges = bridge_edges(G, 'a')
    print bridges
    assert bridges == [('d', 'e')]

test_bridge_edges()

g1=[(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2), (4, 5), (5, 6), (6, 4), (6, 7), (7, 8), (8, 6), (8, 9), (9, 10), (10, 8), (10, 11), (11, 12), (12, 10), (12, 13), (13, 14), (14, 15), (15, 16), (16, 14), (16, 17), (17, 18), (18, 16), (18, 19), (19, 20), (20, 18), (20, 21), (21, 22), (22, 20), (22, 23), (23, 24), (24, 22), (24, 25), (25, 26), (26, 24), (26, 27), (27, 28), (28, 26), (28, 29), (29, 30), (30, 28), (30, 31), (31, 32), (32, 30), (32, 33), (33, 34), (34, 32), (34, 35), (35, 36), (36, 34), (36, 37), (37, 38), (38, 36), (38, 39), (39, 40), (40, 38), (40, 41), (41, 42), (42, 40), (42, 43), (43, 44), (44, 42), (44, 45), (45, 46), (46, 44), (46, 47), (47, 48), (48, 46), (48, 49), (49, 50), (50, 48), (50, 51), (51, 52), (52, 50), (52, 53), (53, 54), (54, 52), (54, 55), (55, 56), (56, 54), (56, 57), (57, 58), (58, 56), (58, 59), (59, 60), (60, 58), (60, 61), (61, 62), (62, 60), (62, 63), (63, 64), (64, 62), (64, 65), (65, 66), (66, 64), (66, 67), (67, 68), (68, 66), (68, 69), (69, 70), (70, 68), (70, 71), (71, 72), (72, 70), (72, 73), (73, 74), (74, 72), (74, 75), (75, 76), (76, 74), (76, 77), (77, 78), (78, 76), (78, 79), (79, 80), (80, 78), (80, 81), (81, 82), (82, 80), (82, 83), (83, 84), (84, 82), (84, 85), (85, 86), (86, 84), (86, 87), (87, 88), (88, 86), (88, 89), (89, 90), (90, 88), (90, 91), (91, 92), (92, 90), (92, 93), (93, 94), (94, 92), (94, 95), (95, 96), (96, 94), (96, 97), (97, 98), (98, 96), (98, 99), (99, 100), (100, 98)]
G1={}
for u,v in g1:
    if u not in G1:
        G1[u]={}
    G1[u][v]=1
    if v not in G1:
        G1[v]={}
    G1[v][u]=1
br2=bridge_edges(G1,0)
assert len(br2)==2
for u,v in br2:
    assert sorted([u,v]) in [[12,13],[13,14]]
