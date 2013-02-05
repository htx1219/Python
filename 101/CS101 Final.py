def remove_tags(t):
    text = t
    result = []
    while text:
        if text[0] == '<':
            g = text.find('>')
            text = text[g+1:]
        elif text.find('<') != -1:
            g = text.find('<')
            result = result + text[:g].split()
            text = text[g:]
        else:
            result = result + text.split()
            text = ''
    return result
    


##print remove_tags('''<h1>Title</h1><p>This is a
##                    <a href="http://www.udacity.com">link</a>.<p>''')
###>>> ['Title','This','is','a','link','.']
##
##print remove_tags('''<table cellpadding='3'>
##                     <tr><td>Hello</td><td>World!</td></tr>
##                     </table>''')
###>>> ['Hello','World!']
##
##print remove_tags("<hello><goodbye>")

def make_converter(match, replacement):
    return lambda x: x.replace(match, replacement, 1) if x.find(match) != -1 else x



def apply_converter(converter, string):
    if string == converter(string):
        return string
    else:
        return apply_converter(converter, converter(string))



# For example,

##c1 = make_converter('aa', 'a')
##print apply_converter(c1, 'aaaa')
###>>> a
##
##c = make_converter('aba', 'b')
##print apply_converter(c, 'aaaaaabaaaaa')

def longest_repetition(l):
    longest = 0
    elt = None
    res = 1
    for i in range(len(l)-1):
        if l[i+1] == l[i]:
            res += 1
        else:
            if res > longest:
                longest = res
                elt = l[i]
            res = 1
    return elt
            
#For example,

##print longest_repetition([1, 2, 2, 3, 3, 3, 2, 2, 1])
### 3
##
##print longest_repetition(['a', 'b', 'b', 'b', 'c', 'd', 'd', 'd'])
### b
##
##print longest_repetition([])
### None



def is_list(p):
    return isinstance(p, list)

def deep_reverse(l):
    new_l = l[:]
    new_l.reverse()
    for i in range(len(new_l)):
        if is_list(new_l[i]):
            new_l[i] = deep_reverse(new_l[i])
    return new_l



#For example,

##p = [1, [2, 3, [4, [5, 6]]]]
##print deep_reverse(p)
###>>> [[[[[6, 5], 4], 3, 2], 1]
##print p
###>>> [1, [2, 3, [4, [5, 6]]]]
##
##q =  [1, [2,3], 4, [5,6]]
##print deep_reverse(q)
###>>> [ [6,5], 4, [3, 2], 1]
##print q
###>>> [1, [2,3], 4, [5,6]]


def stirling(n, k):
    if n==k:
        return 1
    elif n<=k:
        return 0
    elif k==1:
        return 1
    else:
        return k*stirling(n-1, k) + stirling(n-1, k-1)
        
    

def bell(n):
    res = 0
    for i in range(n):
        res += stirling(n, i+1)
    return res

##print stirling(1,1)
###>>> 1
##print stirling(2,1)
###>>> 1
##print stirling(2,2)
###>>> 1
##print stirling(2,3)
###>>>0
##
##print stirling(3,1)
###>>> 1
##print stirling(3,2)
###>>> 3
##print stirling(3,3)
###>>> 1
##
##print stirling(4,1)
###>>> 1
##print stirling(4,2)
###>>> 7
##print stirling(4,3)
###>>> 6
##print stirling(4,4)
###>>> 1
##
##print stirling(5,1)
###>>> 1
##print stirling(5,2)
###>>> 15
##print stirling(5,3)
###>>> 25
##print stirling(5,4)
###>>> 10
##print stirling(5,5)
###>>> 1
##
##print stirling(20,15)
###>>> 452329200
##
##print bell(1)
###>>> 1
##print bell(2)
###>>> 2
##print bell(3)
###>>> 5
##print bell(4)
###>>> 15
##print bell(5)
###>>> 52
##print bell(15)
###>>> 1382958545

def compute_ranks(graph, k):
    d = 0.8 # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node] and nonre(graph, k, node, page):
                    newrank = newrank + d * (ranks[node]/len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


def nonre(graph, k, node, page):
    if k == 0:
        return not node == page
##    elif k == 1:
##        return min([not p == node for p in graph[page]])
    else:
        return min([nonre(graph, k-1, node, p) for p in graph[page]])


# For example

##g = {'a': ['a', 'b', 'c'], 'b':['a'], 'c':['d'], 'd':['a']}
##
##print compute_ranks(g, 0) # the a->a link is reciprocal
###>>> {'a': 0.26676872354238684, 'c': 0.1216391112164609,
###     'b': 0.1216391112164609, 'd': 0.1476647842238683}
##
##print compute_ranks(g, 1) # a->a, a->b, b->a links are reciprocal
###>>> {'a': 0.14761759762962962, 'c': 0.08936469270123457,
###     'b': 0.04999999999999999, 'd': 0.12202199703703702}
##
##print compute_ranks(g, 2)
### a->a, a->b, b->a, a->c, c->d, c->a links are reciprocal
### (so all pages end up with the same rank)
###>>> {'a': 0.04999999999999999, 'c': 0.04999999999999999,
###     'b': 0.04999999999999999, 'd': 0.04999999999999999}

def cellular_automaton(text, pattern, generation):
    dict_p = {'...':1, '..x':2, '.x.':4, '.xx':8, 'x..':16, 'x.x':32, 'xx.':64, 'xxx':128}
    useful = text[-1]+text+text[0]
    p = pattern_trans(pattern)
    result = ''
    for i in range(len(text)):
        if dict_p[useful[i: i+3]] in p:
            result = result + 'x'
        else:
            result = result + '.'
    if generation == 1:
        return result
    else:
        return cellular_automaton(result, pattern, generation-1)
    
def pattern_trans(x):
    res = []
    for i in range(7,-1,-1):
        if x >= 2**i:
            res.append(2**i)
            x = x-2**i
    return res

print cellular_automaton('.x.x.x.x.', 17, 2)
#>>> xxxxxxx..
print cellular_automaton('.x.x.x.x.', 249, 3)
#>>> .x..x.x.x
print cellular_automaton('...x....', 125, 1)
#>>> xx.xxxxx
print cellular_automaton('...x....', 125, 2)
#>>> .xxx....
print cellular_automaton('...x....', 125, 3)
#>>> .x.xxxxx
print cellular_automaton('...x....', 125, 4)
#>>> xxxx...x
print cellular_automaton('...x....', 125, 5)
#>>> ...xxx.x
print cellular_automaton('...x....', 125, 6)
#>>> xx.x.xxx
print cellular_automaton('...x....', 125, 7)
#>>> .xxxxx..
print cellular_automaton('...x....', 125, 8)
#>>> .x...xxx
print cellular_automaton('...x....', 125, 9)
#>>> xxxx.x.x
print cellular_automaton('...x....', 125, 10)
#>>> ...xxxxx
