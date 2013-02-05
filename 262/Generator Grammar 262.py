grammar = [ 
    ("exp", ["exp", "+", "exp"]),
    ("exp", ["exp", "-", "exp"]),
    ("exp", ["(", "exp", ")"]),
    ("exp", ["num"]),
    ]


def expand(tokens, grammar):
    for pos in range(len(tokens)):
        for rule in grammar:
            if rule[0] == tokens[pos]:
                yield tokens[0:pos] + rule[1] + tokens[pos+1:]

def all_pos(depth, start, grammar):
    utterances = [[start]]
    for x in range(depth):
        for sentence in utterances:
            utterances = utterances + [ i for i in expand(sentence, grammar)]
    return utterances

def cfgempty_my_version(grammar,symbol,visited=[], string = []):
    if string == []:
        string = [symbol]
    #print string
    result = []
    for pos in range(len(string)):
        if string[pos] != string[pos].upper():
            pass
        else:
            tried = False
            for i in grammar:
                if grammar.index(i) not in visited and i[0] == string[pos]:
                    tried = True
                    if any([x==x.upper() for x in i[1]]):
                        new_visited =  visited + [grammar.index(i)]
                    else:
                        new_visited = visited
                    #print pos, string,i[1]
                    new_string = string[:pos]+i[1]+string[pos+1:]
                    #print new_string
                    if all([x!=x.upper() for x in new_string]):
                        #print 'new_string append ', new_string
                        result.append(new_string)
                        
                    else:
                        result.append(cfgempty(grammar, new_string[0],new_visited,new_string))
            if not tried: return None
    #print "result!", result
    try:       
        return max(result)
    except ValueError:
        return None

def cfgempty(grammar, symbol, visited = []):
    if symbol in visited:
        return None
    elif not any([ rule[0] == symbol for rule in grammar ]):
        return [symbol]
    else:
        new_visited = visited + [symbol]
        for rhs in [r[1] for r in grammar if r[0] == symbol]:
            if all([None != cfgempty(grammar, r, new_visited) for r in rhs]):
                result = []
                for r in rhs:
                    result = result + cfgempty(grammar, r, new_visited)
                return result
    return None
            

                    
# We have provided a few test cases for you. You will likely want to add
# more of your own. 

grammar1 = [ 
      ("S", [ "P", "a" ] ),           
      ("P", [ "S" ]) ,               
      ] 
                       
print cfgempty(grammar1,"S",[]) == None 

grammar2 = [
      ("S", ["P", "a" ]),             
      ("S", ["Q", "b" ]),             
      ("P", ["P"]), 
      ("Q", ["c", "d"]),              
      ]

print cfgempty(grammar2,"S",[]) == ['c', 'd', 'b']

grammar3 = [  # some Spanish provinces
        ("S", [ "Barcelona", "P", "Huelva"]),
        ("S", [ "Q" ]),
        ("Q", [ "S" ]),
        ("P", [ "Las Palmas", "R", "Madrid"]),
        ("P", [ "T" ]),
        ("T", [ "T", "Toledo" ]),
        ("R", [ ]) ,
        ("R", [ "R"]), 
        ]

print cfgempty(grammar3,"S",[]) == ['Barcelona', 'Las Palmas', 'Madrid', 'Huelva']

def cfginfinite_my_version(grammar): 
    for state in [state[0] for state in grammar]:
        depth = len(grammar)
        utterances = [[state]]
        for x in range(depth):
            for sentence in utterances:
                utterances = utterances + [ i for i in expand(sentence, grammar)]
        for i in utterances:
            if state in i and len(i) != 1:
                return True
    return False

def cfginfinite(grammar):
    for Q in [ rule[0] for rule in grammar ]:
        def helper(current, visited, sizexy):
            if current in visited:
                return sizexy >0
            else:
                new_visited = visited + [current]
                for rhs in [rule[:] for rule in grammar if rule[0] == current]:
                    for symbol in rhs:
                        if helper(symbol, new_visited, sizexy + len(rhs)-1):
                            return True
                return False
        if helper(Q,[],0):
            return True
    return False
    

# We have provided a few test cases. You will likely want to write your own
# as well. 

grammar1 = [ 
      ("S", [ "S", "a" ]), # S -> S a
      ("S", [ "b", ]) , # S -> b 
      ] 
print cfginfinite(grammar1) == True

grammar2 = [ 
      ("S", [ "S", ]), # S -> S 
      ("S", [ "b", ]) , # S -> b 
      ] 

print cfginfinite(grammar2) == False

grammar3 = [ 
      ("S", [ "Q", ]), # S -> Q
      ("Q", [ "b", ]) , # Q -> b
      ("Q", [ "R", "a" ]), # Q -> R a 
      ("R", [ "Q"]), # R -> Q
      ] 

print cfginfinite(grammar3) == True

grammar4 = [  # Nobel Peace Prizes, 1990-1993
      ("S", [ "Q", ]),
      ("Q", [ "Mikhail Gorbachev", ]) ,
      ("Q", [ "P", "Aung San Suu Kyi" ]),
      ("R", [ "Q"]),
      ("R", [ "Rigoberta Tum"]),
      ("P", [ "Mandela and de Klerk"]),
      ] 

print cfginfinite(grammar4) == False

def isambig(grammar, start, utterance):
    enumerated = [ ([start],[]) ]
    while True:
        new_enumerated = enumerated

        for u in enumerated:
            for i in expand(u, grammar):
                if not i in new_enumerated:
                    new_enumerated = new_enumerated + [i]

        if new_enumerated != enumerated:
            enumerated = new_enumerated
        else:
            break
    return len([x for x in enumerated if x[0] == utterance]) > 1

def expand3(tokens_and_derivation, grammar):
    (tokens, derivation) = tokens_and_derivation
    for tokens_pos in range(len(tokens)):
        for rule_index in range(len(grammar)):
            rule = grammar[rule_index]
            if tokens[token_pos] == rule[0]:
                yield ((tokens[0:token_pos] + rule[1] + tokens[token_pos+1]),dereivation+[rule_index])

def isambig_my_version(grammar, start, utterance):
    utterances = [[start]]
    depth = len(grammar)
    for x in range(depth):
        for sentence in utterances:
            new_unt = expand2(sentence, grammar)
            try:
                if len(new_unt)>=1:
                    #print "remove: ", sentence
                    utterances.remove(sentence)
                #print new_unt, sentence
                utterances = utterances + new_unt
            except:
                pass
    print utterances
    key = False
    t = 0
    for i in utterances:
        #print i, utterance
        if i == utterance:
            #print 'pass',t, key
            if t == 0:
                t = 1
                key = False
            elif t>0:
                key = True
            #print t, key
    #print key
    return key

def expand2(tokens, grammar):
    result = []
    for pos in range(len(tokens)):
        for rule in grammar:
            if rule[0] == tokens[pos]:
                result.append(tokens[0:pos] + rule[1] + tokens[pos+1:])
    return result

        

# We have provided a few test cases. You will likely want to add your own.

grammar1 = [ 
       ("S", [ "P", ]),
       ("S", [ "a", "Q", ]) ,
       ("P", [ "a", "T"]),
       ("P", [ "c" ]),
       ("Q", [ "b" ]),
       ("T", [ "b" ]),
       ] 

print isambig(grammar1, "S", ["a", "b"]) == True
print isambig(grammar1, "S", ["c"]) == False

grammar2 = [ 
       ("A", [ "B", ]),
       ("B", [ "C", ]),
       ("C", [ "D", ]),
       ("D", [ "E", ]),
       ("E", [ "F", ]),
       ("E", [ "G", ]),
       ("E", [ "x", "H", ]),
       ("F", [ "x", "H"]),
       ("G", [ "x", "H"]),
       ("H", [ "y", ]),
       ] 
print isambig(grammar2, "A", ["x", "y"]) == True
print isambig(grammar2, "E", ["y"]) == False

grammar3 = [ # Rivers in Kenya
       ("A", [ "B", "C"]),
       ("A", [ "D", ]),
       ("B", [ "Dawa", ]),
       ("C", [ "Gucha", ]),
       ("D", [ "B", "Gucha"]),
       ("A", [ "E", "Mbagathi"]),
       ("A", [ "F", "Nairobi"]),
       ("E", [ "Tsavo" ]),
       ("F", [ "Dawa", "Gucha" ])
       ]

print isambig(grammar3, "A", ["Dawa", "Gucha"]) == True
print isambig(grammar3, "A", ["Dawa", "Gucha", "Nairobi"]) == False
print isambig(grammar3, "A", ["Tsavo"]) == False

