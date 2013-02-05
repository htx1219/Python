def evaluate(ast):
    need_op = []
    env = {}
    for t in ast:
        if t[1] == 'has':
            env[t[0]] = t[2]
        elif t[1] == 'buy':
            need_op.append(t)
        elif t[1] == 'sell':
            buyer = [name for name, buy, item, price in need_op
                     if price == t[3] and item == t[2]]
            if buyer:
                if env[buyer[0]] >= t[3]:
                    env[buyer[0]] -= t[3]
                    env[t[0]] += t[3]
                    need_op.remove([buyer[0], 'buy', t[2], t[3]])
                else:
                    need_op.append(t)
            else:
                need_op.append(t)
    while True:
        op = False
        for t in need_op:
            #print env, need_op
            if t[1] == 'sell':
                buyer = [name for name, buy, item, price in need_op
                         if buy == 'buy' and price == t[3] and item == t[2]]
                if buyer:
                    if env[buyer[0]] >= t[3]:
                        env[buyer[0]] -= t[3]
                        env[t[0]] += t[3]
                        need_op.remove([buyer[0], 'buy', t[2], t[3]])
                        need_op.remove(t)
                        op = True
        if op == False:
            break
    return env


# In test1, exactly one sell happens. Even though klaus still has 25 money
# left over, a "buy"/"sell" only happens once per time it is listed. 
test1 = [ ["klaus","has",50] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ] 

print evaluate(test1) == {'klaus': 25, 'wrede': 105}

# In test2, klaus does not have enough money, so no transactions take place.
test2 = [ ["klaus","has",5] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ] 

print evaluate(test2) == {'klaus': 5, 'wrede': 80}

# Wishful thinking, klaus! Although you want to buy sheep for 5 money and
# you even have 5 money, no one is selling sheep for 5 money. So no
# transactions happen.
test2b = [ ["klaus","has",5] ,
           ["wrede","has",80] ,
           ["klaus","buy","sheep", 5] ,
           ["wrede","sell","sheep", 25] , ] 

print evaluate(test2b) == {'klaus': 5, 'wrede': 80}

# In test3, wrede does not have the 75 required to buy the wheat from
# andreas until after wrede sells the sheep to klaus. 
test3 = [ ["klaus","has",50] ,
          ["wrede","has",50] ,
          ["andreas","has",50] ,
          ["wrede","buy","wheat", 75] ,
          ["andreas","sell","wheat", 75] , 
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , 
          ] 
print evaluate(test3) == {'andreas': 125, 'klaus': 25, 'wrede': 0}

test7 = [ ["klaus","has",50] ,
          ["wrede","has",50] ,
          ["andreas","has",50] ,
          ["wrede","buy","wheat", 75] ,
          ["andreas","sell","wheat", 76] , 
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , 
          ] 
print evaluate(test7) == {'andreas': 50, 'klaus': 25, 'wrede': 75}

test8 = [ ['fred','has',200] ,
          ['bob','has',1000] ,
          ['daniele','has',1000000] ,
          ['fred','buy','computer',500] ,
          ['bob','sell','computer', 500] ,
          ["daniele","buy","sheep", 6000] ,
          ['fred','sell','sheep',800] ,
          ]
#print evaluate(test8) == {'bob': 1500, 'daniele': 999200, 'fred': 500}

test6 = [ ['fred','has',200] ,
          ['bob','has',1000] ,
          ['daniele','has',1000000] ,
          ['fred','buy','computer',500] ,
          ['bob','sell','computer', 501] , #Fred won't buy the computer because he is only offering 500 and its price is 501
          ["daniele","buy","sheep", 6000] ,
          ['fred','sell','sheep',800] ,
          ['fred','sell','goat',300] ,
          ]
#print evaluate(test6) == {'bob': 1000, 'daniele': 999200, 'fred': 1000}

test4 = [ ["klaus","has",50] ,
          ["wrede","has",50] ,
          ["andreas","has",50] ,
          ["wrede","buy","wheat", 75] ,
          ['wrede','buy','iphone',60] ,
          ['wrede','sell','ipad',100] ,
          ["andreas","sell","wheat", 75] , 
          ["klaus","buy","sheep", 25] ,
          ['andreas','buy','ipad', 100] ,
          ['klaus', 'sell', 'iphone', 60] ,
          ["wrede","sell","sheep", 25] , 
          ]
print evaluate(test4) == {'andreas': 25, 'klaus': 85, 'wrede': 40}

test5 = [ ["klaus","has",50] ,
          ["wrede","has",80] ,
          ["wrede","sell","sheep", 25] , 
          ["klaus","buy","sheep", 25] ,
          ]
print evaluate(test5) == {'klaus': 25, 'wrede': 105}
