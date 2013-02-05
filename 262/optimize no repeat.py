def optimize(ast):
    opt = {}
    new_t = []
    for t in ast:
        for k in opt:
            if contain_ident(k, t[1]):
                opt[k] = set()
        remove_ans(opt, t[1])
        try:
            if not contain_ident(t[2], t[1]):
                opt[t[2]] += [t[1]]
                t = t[:2]+(('identifier', opt[t[2]][0]),)
        except:
            opt[t[2]] = [t[1]]
        new_t.append(t)
    return new_t

def contain_ident(k, i):
    if k[0] == 'binop':
        return contain_ident(k[1], i) or contain_ident(k[3], i)
    elif k[0] == 'identifier':
        return k[1] == i

def remove_ans(d, i):
    for k in d:
        if i in d[k]:
            d[k].remove(i)

# We have included some testing code to help you check your work. Since
# this is the final exam, you will definitely want to add your own tests.

example1 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
] 
answer1 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "z", ("identifier", "x")) ,
] 
         
print (optimize(example1)) == answer1

example2 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "a", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
] 

print (optimize(example2)) == example2

example3 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "x", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
] 
answer3 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("identifier", "x")) ,
("assign", "x", ("number", 2)) ,
("assign", "z", ("identifier", "y")) , # cannot be "= x" 
] 

print (optimize(example3)) == answer3

example4 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "z", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
("assign", "b", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
("assign", "z", ("number", 5)) ,
("assign", "p", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "q", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "r", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
] 

answer4 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "z", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
("assign", "b", ("identifier", "z")) ,
("assign", "z", ("number", 5)) ,
("assign", "p", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "q", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "r", ("identifier", "b")) ,
] 

print optimize(example4) == answer4


example5 = [("assign","x",("number",5)),
            ("assign","y",("binop",("identifier","a"),"+",("identifier","b"))),
            ("assign","x",("binop",("identifier","y"),"+",("identifier","z"))),
            ("assign","z",("binop",("identifier","a"),"+",("identifier","b")))]
print optimize(example5) == [('assign', 'x', ('number', 5)), 
('assign', 'y', ('binop', ('identifier', 'a'), '+', ('identifier', 'b'))), 
('assign', 'x', ('binop', ('identifier', 'y'), '+', ('identifier', 'z'))), 
('assign', 'z', ('identifier', 'y'))]


example6 = [ \
("assign", "x", ("binop", ("identifier","x"), "+", ("binop", ("identifier","z"), "+", ("number","1")))),
("assign", "y", ("binop", ("identifier","x"), "+", ("binop", ("identifier","z"), "+", ("number","1"))))
 ]

answer6 =  [ \
("assign", "x", ("binop", ("identifier","x"), "+", ("binop", ("identifier","z"), "+", ("number","1")))),
("assign", "y", ("binop", ("identifier","x"), "+", ("binop", ("identifier","z"), "+", ("number","1"))))
 ]

print optimize(example6)==answer6

example7 = [('assign', 'x', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))), 
('assign', 'e', ("number", 2)), 
('assign', 'z', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c')))]

answer7 = [('assign', 'x', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))), 
('assign', 'e', ("number", 2)), 
('assign', 'z', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c')))]

print optimize(example7) == answer7

ex_self_assign = [ \
    ("assign", "x", ("binop", ("identifier","x"), "+", ('number',1))),
    ("assign", "y", ("binop", ("identifier","x"), "+", ('number',1)))
    ]

an_self_assign =  [ \
    ("assign", "x", ("binop", ("identifier","x"), "+", ('number',1))),
    ("assign", "y", ("binop", ("identifier","x"), "+", ('number',1)))
    ]

print optimize(ex_self_assign)==an_self_assign

example4b = [ \
    ('assign', 'x', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))),
    ('assign', 'e', ("number", 2)),
    ('assign', 'z', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))),
]

answer4b = [ \
    ('assign', 'x', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))),
    ('assign', 'e', ("number", 2)),
    ('assign', 'z', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c')))
]

print optimize(example4b) == answer4b

example4c = [ \
    ('assign', 'x', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))),
    ('assign', 'y', ("identifier", 'e')),
    ('assign', 'z', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))),
]

answer4c = [ \
    ('assign', 'x', ('binop', ('binop', ('binop', ('identifier', 'a'), '+', ('identifier', 'e')), '+', ('identifier', 'b')), '+', ('identifier', 'c'))),
    ('assign', 'y', ("identifier", 'e')),
    ('assign', 'z', ("identifier", 'x'))
]

print optimize(example4c) == answer4c

example5 = [\
   ("assign", "a", ("identifier", "b")) ,
   ("assign", "a", ("identifier", "a")) ,
]

#Some people might believe that a = a should be optimized away. Well, it should practically. But
#this is not allowed under the rules given in the assignment. a = a is not a "subsequent" assignment
#statement for 'a'.
answer5 = [\
    ("assign", "a", ("identifier", "b")) ,
    ("assign", "a", ("identifier", "a")) ,
]

print optimize(example5) == answer5

example6 = [\
    ("assign", "x", ("binop", ("identifier","x"), "+", ("binop", ("identifier","z"), "+", ("number","1")))),
    ("assign", "y", ("binop", ("identifier","x"), "+", ("binop", ("identifier","z"), "+", ("number","1"))))
]
print optimize(example6)

example7 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "d", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
]
answer7 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "d", ("identifier", "y")) ,
("assign", "z", ("identifier", "x")) ,
]

print optimize(example7) == answer7

example8 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "x", ("binop", ("binop", ("identifier","a"), "+", ("identifier","b")), "+", ("number",3))) ,
]
answer8 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "x", ("binop", ("binop", ("identifier","a"), "+", ("identifier","b")), "+", ("number",3))) ,
]

print optimize(example8) == answer8

example9 = [ \
    ("assign", "x", ("binop", ("number","2"), "+", ("number","3"))) ,
    ("assign", "y", ("identifier", 'z')) ,
]
answer9 = [ \
    ("assign", "x", ("binop", ("number","2"), "+", ("number","3"))) ,
    ("assign", "y", ("identifier", 'z')) ,
]

print optimize(example9) == answer9

example10 = [ \
    ('assign', 'a', ('identifier', 'rw')),
    ('assign', 'q', ('identifier', 'rw')),
    ('assign', 'x', ('binop', ('identifier', 'a'), '+', ('identifier', 'b'))),
    ('assign', 'y', ('binop', ('identifier', 'a'), '+', ('identifier', 'b'))),
]

answer10 = [ \
    ('assign', 'a', ('identifier', 'rw')),
    ('assign', 'q', ('identifier', 'a')),
    ('assign', 'x', ('binop', ('identifier', 'a'), '+', ('identifier', 'b'))),
    ('assign', 'y', ('identifier', 'x')),
]

print optimize(example10) == answer10

example11 = [ \
    ('assign', 'a', ('number', '11')),
    ('assign', 'b', ('identifier', 'a')),
    ('assign', 'a', ('identifier', 'a')),
]
answer11 = [ \
    ('assign', 'a', ('number', '11')),
    ('assign', 'b', ('identifier', 'a')),
    ('assign', 'a', ('identifier', 'b')),
]

print optimize(example11) == answer11

example12 = [ \
    ("assign", "x", ("identifier","y") ),
    ("assign", "z", ("identifier","y") ),
    ("assign", "y", ("number", 5)),
    ("assign", "p", ("identifier","x") ),
    ("assign", "z", ("identifier","y") ),
    ("assign", "z", ("identifier","x") )
 ]

# Here are the possible optimizations that I can see. Not sure which one(s) is right.
# I think maybe answer12_poss1 is correct based on the specs given BUT answer12_poss3 is VERY possible.
answer12_poss1 = [ \
    ("assign", "x", ("identifier","y") ),
    ("assign", "z", ("identifier","x") ), #This is the first optimization based on the specs given
    ("assign", "y", ("number", 5)),
    ("assign", "p", ("identifier","x") ),
    ("assign", "z", ("identifier","y") ),
    ("assign", "z", ("identifier","p") )  #This is the last optimization based on the specs given
 ]

answer12_poss2 = [ \
    ("assign", "x", ("identifier","y") ),
    ("assign", "z", ("identifier","x") ), #This is the first optimization based on the specs given
    ("assign", "y", ("number", 5)),
    ("assign", "p", ("identifier","x") ),
    ("assign", "z", ("number","5") ), # y = 5, but 5 does not fit the var1 = rhs, var2 = rhs -- thus var1 = var2 mantra in the spec. So is this valid?
    ("assign", "z", ("identifier","p") )  #This is the last optimization based on the specs given
 ]

answer12_poss3 = [ \
    ("assign", "x", ("identifier","y") ),
    ("assign", "z", ("identifier","x") ), #This is the first optimization based on the specs given
    ("assign", "y", ("number", 5)),
    ("assign", "p", ("identifier","z") ), #Why this optimization? Well, because we optimized z = y to z = x. So now z = x. Thus with p = x, we have x on the RHS twice without x changing. Thus p = z via var1 = rhs, var2 = rhs ... var1 = var2
    ("assign", "z", ("identifier","y") ), 
    ("assign", "z", ("identifier","p") )  #This is the last optimization based on the specs given
 ]
print optimize(example12) ==  answer12_poss1  # According to Peter, this should return TRUE
print optimize(example12) ==  answer12_poss2  # This should return FALSE
print optimize(example12) ==  answer12_poss3  # This should return FALSE


