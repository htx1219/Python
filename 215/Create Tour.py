from random import choice

def create_tour(nodes):
    # your code here
    return [(nodes[i-1], nodes[i]) for i in range(len(nodes))]

#########

def get_degree(tour):
    degree = {}
    for x, y in tour:
        degree[x] = degree.get(x, 0) + 1
        degree[y] = degree.get(y, 0) + 1
    return degree

def check_edge(t, b, nodes):
    """
    t: tuple representing an edge
    b: origin node
    nodes: set of nodes already visited

    if we can get to a new node from `b` following `t`
    then return that node, else return None
    """
    if t[0] == b:
        if t[1] not in nodes:
            return t[1]
    elif t[1] == b:
        if t[0] not in nodes:
            return t[0]
    return None

def connected_nodes(tour):
    """return the set of nodes reachable from
    the first node in `tour`"""
    a = tour[0][0]
    nodes = set([a])
    explore = set([a])
    while len(explore) > 0:
        # see what other nodes we can reach
        b = explore.pop()
        for t in tour:
            node = check_edge(t, b, nodes)
            if node is None:
                continue
            nodes.add(node)
            explore.add(node)
    return nodes

def is_eulerian_tour(nodes, tour):
    # all nodes must be even degree
    # and every node must be in graph
    degree = get_degree(tour)
    for node in nodes:
        try:
            d = degree[node]
            if d % 2 == 1:
                print "Node %s has odd degree" % node
                return False
        except KeyError:
            print "Node %s was not in your tour" % node
            return False
    connected = connected_nodes(tour)
    if len(connected) == len(nodes):
        return True
    else:
        print "Your graph wasn't connected"
        return False

def find_odd_nodes(graph):
    degree = get_degree(graph)
    odd = []
    for k in degree.keys():
        if degree[k] % 2 == 1:
            odd.append(k)
    return odd

def test():
    nodes = [20, 21, 22, 23, 24, 25]
    tour = create_tour(nodes)
    return is_eulerian_tour(nodes, tour)

def find_nodes(node, graph):
    res = []
    for k in graph:
        if k[0] == node:
            res.append(k[1])
        elif k[1] == node:
            res.append(k[0])
    return res

def find_eulerian_tour_random(graph):
    path = [graph[0]]
    while len(path) != len(graph):
        start = path[-1][1]
        nodes = find_nodes(start, graph)
        if min([((start, second) in path or (second, start) in path) for second in nodes]) != False:
            path = [graph[0]]
            continue
        second = choice(nodes)
        while (start, second) in path or (second, start) in path:
            second = choice(nodes)
        path.append((start, second))
    return [p[0] for p in path]+[graph[0][0]]

def sort_nodes(nodes, path):
    p = [k[0] for k in path]+[path[-1][1]]
    not_s = [n for n in nodes if n not in p]
    s = [n for n in nodes if n in p]
    return not_s+s
    

def find_eulerian_tour(graph, path = None):
    if path == None:
        odd = find_odd_nodes(graph)
        if not odd:
            path = [graph[0]]
        if odd:
            return None
            assert len(odd) == 2
            start = odd[0]
            nodes = find_nodes(start, graph)
            not_odd = [n for n in nodes if n != odd[1]]
            path = [(odd[0], not_odd[0])]
    if len(path) != len(graph):
        start = path[-1][1]
        nodes = find_nodes(start, graph)
##        if min([((start, second) in path or (second, start) in path) for second in nodes]) != False:
##            return None
##        s_nodes = sort_nodes(nodes, path)
        for i in nodes:
            if (start, i) in path or (i, start) in path:
                continue
            new_p = path + [(start, i)]
            #print start, i
            final_p = find_eulerian_tour(graph, new_p)
            if final_p:
                return final_p
        return None
    else:
        return [p[0] for p in path]+[graph[0][0]]

toygraph = [(1, 2), (2, 3), (3, 1)]
print find_eulerian_tour(toygraph)

hard1 = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2), (4, 5), (5, 6), (6, 4), (6, 7), (7, 8), (8, 6), (8, 9), (9, 10), (10, 8), (10, 11), (11, 12), (12, 10), (12, 13), (13, 14), (14, 12), (14, 15), (15, 16), (16, 14), (16, 17), (17, 18), (18, 16), (18, 19), (19, 20), (20, 18), (20, 21), (21, 22), (22, 20), (22, 23), (23, 24), (24, 22), (24, 25), (25, 26), (26, 24), (26, 27), (27, 28), (28, 26), (28, 29), (29, 30), (30, 28), (30, 31), (31, 32), (32, 30), (32, 33), (33, 34), (34, 32), (34, 35), (35, 36), (36, 34), (36, 37), (37, 38), (38, 36), (38, 39), (39, 40), (40, 38), (40, 41), (41, 42), (42, 40), (42, 43), (43, 44), (44, 42), (44, 45), (45, 46), (46, 44), (46, 47), (47, 48), (48, 46), (48, 49), (49, 50), (50, 48), (50, 51), (51, 52), (52, 50), (52, 53), (53, 54), (54, 52), (54, 55), (55, 56), (56, 54), (56, 57), (57, 58), (58, 56), (58, 59), (59, 60), (60, 58), (60, 61), (61, 62), (62, 60), (62, 63), (63, 64), (64, 62), (64, 65), (65, 66), (66, 64), (66, 67), (67, 68), (68, 66), (68, 69), (69, 70), (70, 68), (70, 71), (71, 72), (72, 70), (72, 73), (73, 74), (74, 72), (74, 75), (75, 76), (76, 74), (76, 77), (77, 78), (78, 76), (78, 79), (79, 80), (80, 78), (80, 81), (81, 82), (82, 80), (82, 83), (83, 84), (84, 82), (84, 85), (85, 86), (86, 84), (86, 87), (87, 88), (88, 86), (88, 89), (89, 90), (90, 88), (90, 91), (91, 92), (92, 90), (92, 93), (93, 94), (94, 92), (94, 95), (95, 96), (96, 94), (96, 97), (97, 98), (98, 96), (98, 99), (99, 100), (100, 98)]
print find_eulerian_tour(hard1)

hard2 = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2), (4, 5), (5, 6), (6, 4), (6, 7), (7, 8), (8, 6), (8, 9), (9, 10), (10, 8), (10, 11), (11, 12), (12, 10), (12, 13), (13, 14), (14, 15), (15, 16), (16, 14), (16, 17), (17, 18), (18, 16), (18, 19), (19, 20), (20, 18), (20, 21), (21, 22), (22, 20), (22, 23), (23, 24), (24, 22), (24, 25), (25, 26), (26, 24), (26, 27), (27, 28), (28, 26), (28, 29), (29, 30), (30, 28), (30, 31), (31, 32), (32, 30), (32, 33), (33, 34), (34, 32), (34, 35), (35, 36), (36, 34), (36, 37), (37, 38), (38, 36), (38, 39), (39, 40), (40, 38), (40, 41), (41, 42), (42, 40), (42, 43), (43, 44), (44, 42), (44, 45), (45, 46), (46, 44), (46, 47), (47, 48), (48, 46), (48, 49), (49, 50), (50, 48), (50, 51), (51, 52), (52, 50), (52, 53), (53, 54), (54, 52), (54, 55), (55, 56), (56, 54), (56, 57), (57, 58), (58, 56), (58, 59), (59, 60), (60, 58), (60, 61), (61, 62), (62, 60), (62, 63), (63, 64), (64, 62), (64, 65), (65, 66), (66, 64), (66, 67), (67, 68), (68, 66), (68, 69), (69, 70), (70, 68), (70, 71), (71, 72), (72, 70), (72, 73), (73, 74), (74, 72), (74, 75), (75, 76), (76, 74), (76, 77), (77, 78), (78, 76), (78, 79), (79, 80), (80, 78), (80, 81), (81, 82), (82, 80), (82, 83), (83, 84), (84, 82), (84, 85), (85, 86), (86, 84), (86, 87), (87, 88), (88, 86), (88, 89), (89, 90), (90, 88), (90, 91), (91, 92), (92, 90), (92, 93), (93, 94), (94, 92), (94, 95), (95, 96), (96, 94), (96, 97), (97, 98), (98, 96), (98, 99), (99, 100), (100, 98)]
print find_eulerian_tour(hard2)

hard3 = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0), (0, 5), (5, 6), (6, 0), (0, 7), (7, 8), (8, 0), (0, 9), (9, 10), (10, 0), (0, 11), (11, 12), (12, 0), (0, 13), (13, 14), (14, 0)]
print find_eulerian_tour(hard3)
