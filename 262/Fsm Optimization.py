import copy

def nfsmtrim(edges_old, accepting_old):
    edges = copy.deepcopy(edges_old)
    accepting = accepting_old[:]
    for item in edges.items():
        for i in item[1]:
            if not nfsmaccepts(i, edges, accepting, []):
                item[1].remove(i)
        if item[1] == []:
            edges.pop(item[0])
    for i in accepting:
        if [i] not in edges.values():
            accepting.remove(i)
    return edges, accepting

def nfsmaccepts(current, edges, accepting, visited):
    if current in visited:
        return None
    elif current in accepting:
        return "o"
    else:
        newvisited = visited + [current]
        for edge in edges:
            if edge[0] == current:
                for newstate in edges[edge]:
                    foo = nfsmaccepts(newstate, edges, accepting, newvisited)
                    if foo != None:
                        return edge[1]+foo      

# We have included a few test cases, but you will definitely want to make
# your own. 

edges1 = { (1,'a') : [1] ,
           (1,'b') : [2] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (8,'z') : [9] , } 
accepting1 = [ 1 ]

(new_edges1, new_accepting1) = nfsmtrim(edges1,accepting1)

print new_edges1, new_accepting1
print "Test 1"
print new_edges1 == {(1, 'a'): [1]}
print new_accepting1 == [1]
print edges1, accepting1

(new_edges2, new_accepting2) = nfsmtrim(edges1,[]) 
print 'test 2'
print new_edges2 == {}
print new_accepting2 == []

(new_edges3, new_accepting3) = nfsmtrim(edges1,[3,6]) 
print 'test 3'
print edges1
print new_edges3
print new_edges3 == {(1, 'a'): [1], (1, 'b'): [2], (2, 'b'): [3]}
print new_accepting3 == [3]

edges4 = { (1,'a') : [1] ,
           (1,'b') : [2,5] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (3,'c') : [2,1,4] } 
accepting4 = [ 2 ] 
(new_edges4, new_accepting4) = nfsmtrim(edges4, accepting4) 
print 'test 4'
print new_edges4 == { 
  (1, 'a'): [1],
  (1, 'b'): [2], 
  (2, 'b'): [3], 
  (3, 'c'): [2, 1], 
}
print new_accepting4 == [2]

