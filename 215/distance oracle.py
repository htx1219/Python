def create_labels(G, root):
    labels = {}
    labels[root] = {root:0}
    need_search = [root]
    while need_search:
        node = need_search.pop(0)
        for node2 in G[node]:
            if node2 not in labels:
                labels[node2] = dict([(node2, 0)]+[(n, k+1) for n, k in labels[node].items()])
                need_search.append(node2)
    return labels

def create_labels2(G):
    root = G.keys()[0]
    labels = {}
    labels[root] = {root:0}
    need_search = [root]
    while need_search:
        node = need_search.pop(0)
        for node2 in G[node]:
            if node2 not in labels:
                labels[node2] = dict([(node2, 0)]+[(n, k+1) for n, k in labels[node].items()])
                need_search.append(node2)
    return labels

#######
# Testing
#

def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test():
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree, 2)
    distances = get_distances(tree, labels)
    print distances
    labels = create_labels2(tree)
    distances = get_distances(tree, labels)
    print distances
    assert distances[1][2] == 1
    assert distances[1][4] == 2
    assert distances[1][2] == 1
    assert distances[1][4] == 2

    assert distances[4][1] == 2
    assert distances[1][4] == 2
    assert distances[2][1] == 1
    assert distances[1][2] == 1

    assert distances[1][1] == 0
    assert distances[2][2] == 0
    assert distances[9][9] == 0
    assert distances[2][3] == 2
    assert distances[12][13] == 2
    assert distances[13][8] == 6
    assert distances[11][12] == 6
    assert distances[1][12] == 3

    print 'test pass'

test()
