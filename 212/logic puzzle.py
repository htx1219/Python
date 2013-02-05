import itertools

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    arrivals = Mon, Tue, Wed, Thu, Fri = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(arrivals))
    ans = next((Hamming, Knuth, Minsky, Simon, Wilkes)
               for (laptop, droid, tablet, iphone, buy) in orderings
               if laptop == Wed
               if tablet != Fri
               if iphone == Tue or tablet == Tue
               for (programmer, writer, manager, designer, work) in orderings
               if tablet != manager
               if designer != droid
               if designer != Thu
               for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings
               if programmer != Hamming
               if writer != Minsky
               if Knuth != manager
               if Knuth-Simon == 1
               if Knuth - manager == 1
               if one_of((programmer, droid), (Wilkes, Hamming))
               if one_of((laptop, Wilkes), (Mon, writer)))

    return trans_ans(ans)

def trans_ans(ans):
    res = ['','','','','']
    a_dict = {0:'Hamming', 1:'Knuth', 2:'Minsky', 3:'Simon', 4:'Wilkes'}
    for i, j in enumerate(ans):
        res[j-1] = a_dict[i]
    return res

def one_of(q, w):
    return (((q[1]==w[1] and q[0]==w[0]) or (q[1]==w[0] and w[1]==q[0]))
            and q[0] != q[1] and w[0] != w[1])

print logic_puzzle()
