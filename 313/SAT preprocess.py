def sat_preprocessing(num_variables, clauses):
    # YOUR CODE HERE
    times = [0]*num_variables
    sign = [0]*num_variables
    for i in range(0, len(clauses)):
        if len(clauses[i]) == 1:
            var = clauses[i][0]
            clauses = set_var(clauses, var)
            return sat_preprocessing(num_variables, clauses)
        
    for i in range(0, len(clauses)):
        if len(clauses[i]) == 0:
            return [[1, -1]]

    for i in clauses:
        for v in i:
            times[abs(v)-1] += 1
            sign[abs(v)-1] = (v>0)
    for w in range(0, len(times)):
        if times[w] == 1:
            var = (2*sign[w]-1) * (w+1)
            clauses = set_var(clauses, var)
            return sat_preprocessing(num_variables, clauses)
            
    return clauses

def set_var(clauses, var):
    for j in range(0, len(clauses)):
        for v in range(0, len(clauses[j])):
            if abs(clauses[j][v]) == abs(var):
                if clauses[j][v]==var:
                    clauses = clauses[0:j] + clauses[j+1:len(clauses)]
                    return set_var(clauses, var)
                else:
                    clauses[j] = clauses[j][0:v] + clauses[j][v+1:len(clauses[j])]
                    return set_var(clauses, var)
    return clauses

def test():
    assert [] == sat_preprocessing(1, [[1]])
    assert [[1,-1]] == sat_preprocessing(1, [[1], [-1]])
    assert [] == sat_preprocessing(4, [[4], [-3, -1], [3, -4, 2, 1], [1, -3, 4],
                                         [-1, -3, -4, 2], [4, 3, 1, 2], [4, 3],
                                         [1, 3, -4], [3, -4, 1], [-1]])
    assert [[1,-1]] == sat_preprocessing(5, [[4, -2], [-1, -2], [1], [-4],
                                         [5, 1, 4, -2, 3], [-1, 2, 3, 5],
                                         [-3, -1], [-4], [4, -1, 2]])
    ans = [[5, 6, 2, 4], [3, 5, 2, 4], [-5, 2, 3], [-3, 2, -5, 6, -4]]
    assert ans == sat_preprocessing(6, [[-5, 3, 2, 6, 1], [5, 6, 2, 4],
                                        [3, 5, 2, -1, 4], [1], [2, 1, 4, 3, 6],
                                        [-1, -5, 2, 3], [-3, 2, -5, 6, -4]])
    print "test pass"
    
test()
