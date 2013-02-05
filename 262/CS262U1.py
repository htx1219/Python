import re

def myfirst_yoursecond(p, q):
    p_space = p.find(" ")
    q_space = q.find(" ")
    p2= q.split()
    return p[:p_space] == q[q_space+1:]

c1 = re.findall(r"[0-9]", '1+2==3')

c2 = re.findall(r"[a-c]", "Barbara Liskov")
c3 = re.findall(r"-?[a-z]*|[0-9]+", "Gorthe 1789")
regexp = r"(?:do|re|mi)*"


edges = { (1, 'a') : [2, 3],
          (2, 'a') : [2],
          (3, 'b') : [4, 3],
          (4, 'c') : [5] }
accepting = [2, 5] 

def nfsmsim(string, current, edges, accepting):
    possible = []
    if string == '':
        return current in accepting
    else:
        letter = string[0]
        if (current, letter) in edges:
            for i in range(0, len(edges[(current,letter)])):
                possible.append(nfsmsim(string[1:], edges[(current,letter)][i], edges, accepting))
            return max(possible)
        else:
            return False
            
def test_nfsmsim():
    print "Test case 1 passed: " + str(nfsmsim("abc", 1, edges, accepting) == True) 
    print "Test case 2 passed: " + str(nfsmsim("aaa", 1, edges, accepting) == True) 
    print "Test case 3 passed: " + str(nfsmsim("abbbc", 1, edges, accepting) == True) 
    print "Test case 4 passed: " + str(nfsmsim("aabc", 1, edges, accepting) == False) 
    print "Test case 5 passed: " + str(nfsmsim("", 1, edges, accepting) == False) 

edges = { (1, 'a') : [2, 3],
          (2, 'a') : [2],
          (3, 'b') : [4, 2],
          (4, 'c') : [5] }
accepting = [5] 

edges2 = { (1, 'a') : [1],
           (2, 'a') : [2] }
accepting2 = [2] 
"""
def nfsmaccepts(current, edges, accepting, visited):
    s = ''
    return nfsmaccepts_recor(current, edges, accepting, visited, s)    
    
def nfsmaccepts_recor(current, edges, accepting, visited, s):
    if current in accepting:
        return s
    allcon = [None]
    for i in edges.keys():
        if i[0] == current:
            if current not in visited:
                visited.append(current)
            notend = []
            for j in edges[i]:
                notend.append(j in visited)
            if min(notend) == True:
                return None
            s = s + i[1]
            for j in edges[i]:
                allcon.append(nfsmaccepts_recor(j, edges, accepting, visited, s))
            return max(allcon)
"""
def nfsmaccepts(current, edges, accepting, visited, s=""):
    if current in accepting:
        return s
    allcon = [None]
    for i in edges.keys():
        if i[0] == current:
            if current not in visited:
                visited.append(current)
            notend = []
            for j in edges[i]:
                notend.append(j in visited)
            if min(notend) == True:
                return None
            s = s + i[1]
            for j in edges[i]:
                allcon.append(nfsmaccepts(j, edges, accepting, visited, s))
            return max(allcon)

def test_nfsmaccepts():
    print "Test 1: " + str(nfsmaccepts(1, edges, accepting, []) == "abc") 
    print "Test 2: " + str(nfsmaccepts(1, edges, [4], []) == "ab") 
    print "Test 3: " + str(nfsmaccepts(1, edges2, accepting2, []) == None) 
    print "Test 4: " + str(nfsmaccepts(1, edges2, [1], []) == "")

test_nfsmaccepts()
    
