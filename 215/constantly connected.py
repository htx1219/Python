def mark_component(G, node, marked, H):
    marked[node] = True
    total_marked = 1
    for neighbor in G[node]:
        if neighbor not in marked:
            total_marked += mark_component(G, neighbor, marked, H)
    H[node] = marked
    return total_marked

def process_graph(G):
    global H
    H = {}
    for node in G:
        if node not in H:
            marked = {}
            mark_component(G, node, marked, H)
    G['is_connected'] = H
    return

#
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick
#
def is_connected(i, j):
    return j in H[i]
    pass

#######
# Testing
#
def test():
    G = {1:{2:1},
         2:{1:1},
         3:{4:1},
         4:{3:1},
         5:{}}
    process_graph(G)
    assert is_connected(1, 2) == True
    assert is_connected(1, 3) == False

    G = {1:{2:1, 3:1},
         2:{1:1},
         3:{4:1, 1:1},
         4:{3:1},
         5:{}}
    process_graph(G)
    assert is_connected(1, 2) == True
    assert is_connected(1, 3) == True
    assert is_connected(1, 5) == False

    print 'test pass'

test()
