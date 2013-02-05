from copy import deepcopy
import cProfile
import resource

toygraph_old = [("1",["4"]),
            ("2",["7"]),
            ("3",["9"]),
            ("4",["1"]),
            ("5",["8"]),
            ("6",["3",'8']),
            ("7",["5"]),
            ("8",["2"]),
            ("9",["4","6","10"]),
            ("11",["1"])]

maxnode = 11

toygraph = [["4"],["7"],["9"],["1"],["8"],["3"],
            ["5"],["2","6"],["4","6"]]

toyedges = [("1","4"),("4","1"),("9","4"),("3","9"),("9","6"),("6","3"),
            ("6","8"),("8","2"),("2","7"),("7","5"),("5","8"),("9","10"),("11","1")]

def count_scc(edges, graph, print_res = False):
    count = []
    rev_graph = {}
    for nodes in edges:
        if nodes[1] not in rev_graph:
            rev_graph[nodes[1]]=[nodes[0]]
        else:
            rev_graph[nodes[1]] += [nodes[0]]
    rev_graph = rev_graph.items()
    sort_by_key = lambda x: int(x[0])
    rev_graph.sort(key=sort_by_key)
    print len(rev_graph)
    rev = set_reverse(rev_graph)
    print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print "reverse done"
    explored = []
    def depth_first_search(graph, i):
        explored.append(i)
        to_explore = [i]       
        while to_explore:
            k = to_explore.pop()
            frontier = graph_find(graph, k)
            if frontier:
                for j in frontier:
                    if j not in explored:
                        explored.append(j)
                        to_explore.append(j)
    for i in range(maxnode):
        if i % 50000 == 0:
            print i, ' times'
        q = find_list(rev, max(rev))
        pre = len(explored)
        if str(q) not in explored:
            depth_first_search(graph, str(q))
            after = len(explored)
            count.append(after-pre)
        rev[q] = 0
    count.sort(reverse = True)
    print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return count[:5]
        
def find_list(l, e):
    for (i, j) in enumerate(l):
        if j == e:
            return i

def set_reverse(graph, print_res = False):
    global t
    t = 0
    explored = []
    print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    finished = [0]*(maxnode+1)
    def depth_first_search(graph, i):
        global t, s
        explored.append(i)
        to_explore = [i]       
        while to_explore:
            complete = True
            k = to_explore[-1]
            frontier = graph_find(graph, k)
            if frontier:
                for j in frontier:
                    if j not in explored:
                        complete = False
                        explored.append(j)
                        to_explore.append(j)
            if complete:
                to_explore.pop()
                t += 1
                finished[int(k)] = t
##        frontier = graph_find(graph, i)
##        if frontier:
##            for j in frontier:
##                if j not in explored:
##                    depth_first_search(graph, j)
##        t += 1
##        finished[int(i)] = t
    for i in range(maxnode,0, -1):
        if i % 50000 == 0:
            print i, ' times'
            print len(explored), 'items explored'
            print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if str(i) not in explored:
            s = str(i)
            depth_first_search(graph, str(i))
    return finished

def graph_find(graph, node):
    for k in graph:
        if k[0] == node:
            return k[1]

print set_reverse(toygraph_old)
print count_scc(toyedges, toygraph_old)

#cProfile.run("count_scc(toyedges, toygraph_old)")

explored = []
def depth_first_search(graph, i):
    explored.append(i)
    to_explore = [i]       
    while to_explore:
        k = to_explore.pop()
        frontier = graph_find(graph, k)
        if frontier:
            for j in frontier:
                if j not in explored:
                    explored.append(j)
                    to_explore.append(j)

depth_first_search(toygraph_old, '8')
print len(explored)

nums = open("SCC.txt")
edges = []
graph = []
line = nums.readline()
while line:
    nodes = line.split()
    edges.append((nodes[0],nodes[1]))
    if not graph:
        graph.append([nodes[0], [nodes[1]]])
    elif graph[-1][0] == nodes[0]:
        graph[-1][1] += [nodes[1]]
    else:
        graph.append([nodes[0], [nodes[1]]])
    line = nums.readline()
print len(edges), len(graph)
print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

explored = []
depth_first_search(graph, '1')
print len(explored)

maxnode = 875714
print count_scc(edges, graph)
    

            
    
