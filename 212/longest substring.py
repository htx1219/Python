chart = { }

def csuffix(X,Y):
    try:
        return chart[X,Y]
    except:
        if X[-1:] != Y[-1:]:
            chart[(X,Y)] = 0
        elif len(X) <= 0 or len(Y) <= 0:
            return 0
        else:
            chart[(X,Y)] = 1 + csuffix(X[:-1], Y[:-1])
        return chart[(X,Y)]

def prefixes(X):
    return [X[:n+1] for n in range(len(X))]

def lsubstring(X,Y):
    return max([csuffix(x, y) for x in prefixes(X) for y in prefixes(Y)])

# We have included some test cases. You will likely want to write your own.

print lsubstring("Tapachula", "Temapache") == 5  # Mexico, "apach"
print chart[("Tapach","Temapach")] == 5
print lsubstring("Harare", "Mutare") == 3        # Zimbabwe, "are" 
print chart[("Harare","Mutare")] == 3
print lsubstring("Iqaluit", "Whitehorse") == 2   # Canada, "it" 
print chart[("Iqaluit","Whit")] == 2
print lsubstring("Prey Veng", "Svay Rieng") == 3 # Cambodia, "eng" 
print chart[("Prey Ven","Svay Rien")] == 2
print chart[("Prey Veng","Svay Rieng")] == 3
print lsubstring("Aceh", "Jambi") == 0           # Sumatra, ""
print chart[("Aceh", "Jambi")] == 0

