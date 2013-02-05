def greedy_vc(input_graph):
    # YOUR CODE HERE
    cover = []
    valid, num_edge = valid_cover(input_graph, cover)
    
    while not valid:
        m = [x for x in range(0, len(num_edge)) if num_edge[x] == max(num_edge)][0]
        cover.append(m)
        valid, num_edge = valid_cover(input_graph, cover)
        
    return cover

def valid_cover(graph, cover):
    valid = True
    num_edge = [0] * len(graph)
    for i in range(0, len(graph)):
        for j in range(i, len(graph)):
            if graph[i][j] == 1:
                if (i not in cover) and (j not in cover):
                    valid = False
                    num_edge[i] += 1
                    num_edge[j] += 1
    return valid, num_edge

def test():
    graph = [[0, 1, 1, 1, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 1, 1],
             [1, 0, 1, 0, 1],
             [1, 1, 1, 1, 0]]
    cover = greedy_vc(graph)
    print cover
    # There are multiple possible right answers
    assert (cover == [0, 4, 2] or
            cover == [0, 4, 3] or
            cover == [4, 0, 2] or
            cover == [4, 0, 3])
    
test()
