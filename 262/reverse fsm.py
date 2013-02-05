edges = { (1,'a') : [2],
          (2,'b') : [3,4],
          (3,'x') : [5],
          (4,'y') : [5],
          (5,'b') : [3,4], 
          (5,'c') : [6],
          } 
accepting = 6 
start = 1

def reverse(edges,accepting,start): 
    l_edge = list(edges.items())
    r_edge = {}
    for i in l_edge:
        for des in i[1]:
            try:
                r_edge[(des, i[0][1])] += [i[0][0]]
            except:
                r_edge[(des, i[0][1])] = [i[0][0]]
    return (r_edge, start, accepting)
                

# We have included some testing code to help you check your work. Since
# this is the final exam, you will definitely want to add your own tests.
#
# Recall: "hello"[::-1] == "olleh" 

def nfsmaccepts(edges,accepting,current,str): 
        if str == "":
                return current == accepting
        letter = str[0]
        rest = str[1:] 
        if (current,letter) in edges:
                for dest in edges[(current,letter)]:
                        if nfsmaccepts(edges,accepting,dest,rest):
                                return True
        return False
        
r_edges, r_accepting, r_start = reverse(edges,accepting,start) 
print r_edges

for s in [ "abxc", "abxbyc", "not", "abxbxbxbxbxc", "" ]: 
        # The original should accept s if-and-only-if the
        # reversed version accepts s_reversed.
        print nfsmaccepts(edges,accepting,start,s)==nfsmaccepts(r_edges,r_accepting,r_start,s[::-1])

# r"a+b*"
edges2 = { (1,'a') : [2],
          (2,'a') : [2],
          (2,'b') : [2] 
          } 
accepting2 = 2 
start2 = 1 

r_edges2, r_accepting2, r_start2 = reverse(edges2,accepting2,start2) 
print r_edges2

for s in [ "aaaab", "aabbbbb", "ab", "b", "a", "", "ba" ]:
    print nfsmaccepts(edges2,accepting2,start2,s)== nfsmaccepts(r_edges2,r_accepting2,r_start2,s[::-1])
