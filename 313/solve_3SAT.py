# Take any clause that is not satisfied
# * If all variables have already been set, then there is no
#   possible solution anymore
# * Otherwise, branch into at most three cases where in each case a different
#   variable is set so that the clause becomes satisfied:
#  - The first variable is set so that clause becomes satisfied
#    (and we don't do anything with the other variables)
#  - The first variable is set so that clause does not becomes satisfied,
#    the second one is set so that it becomes satisfied and we don't do
#    anything with the third variable.
#  - The first and second variable are set so that the clause does not
#    become satisfied, the third one is set so that it does become satisfed.

# Note that any solution must fall into one of the above categories.
# Naturally, after having applied the pre-processing and also during the
# branching, some clauses will not contain three unassigned variables anymore
# and your program needs to account for that.

from copy import deepcopy

def sat_preprocessing(num_variables, clauses, assignment=None):
    # YOUR CODE HERE
    times = [0]*num_variables
    sign = [0]*num_variables
    if assignment == None:
        assignment = [-1]*(num_variables+1)
    for i in range(0, len(clauses)):
        if len(clauses[i]) == 1:
            var = clauses[i][0]
            clauses = set_var(clauses, var)
            assignment[abs(var)] = (var>0)
            return sat_preprocessing(num_variables, clauses, assignment)
        
    for i in range(0, len(clauses)):
        if len(clauses[i]) == 0:
            return [[1, -1]], assignment

    # sign = 0:unseen 1:all pos -1: all neg 2:pos & neg
    for i in clauses:
        for v in i:
            if sign[abs(v)-1] == 0:
                times[abs(v)-1] += 1
                sign[abs(v)-1] = 2*(v>0) - 1
            elif 2*(v>0)-1 != sign[abs(v)-1]:
                times[abs(v)-1] += 1
                sign[abs(v)-1] = 2
            
    for w in range(0, len(times)):
        if times[w] == 1:
            var = sign[w] * (w+1)
            clauses = set_var(clauses, var)
            assignment[abs(var)] = (var>0)
            return sat_preprocessing(num_variables, clauses, assignment)
            
    return (clauses, assignment)

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

def testperp():
    print sat_preprocessing(1, [[1]])
    print sat_preprocessing(1, [[1], [-1]])
    print sat_preprocessing(4, [[4], [-3, -1], [3, -4, 2, 1], [1, -3, 4],
                                         [-1, -3, -4, 2], [4, 3, 1, 2], [4, 3],
                                         [1, 3, -4], [3, -4, 1], [-1]])
    print sat_preprocessing(5, [[4, -2], [-1, -2], [1], [-4],
                                         [5, 1, 4, -2, 3], [-1, 2, 3, 5],
                                         [-3, -1], [-4], [4, -1, 2]])
    ans = [[5, 6, 2, 4], [3, 5, 2, 4], [-5, 2, 3], [-3, 2, -5, 6, -4]]
    print sat_preprocessing(6, [[-5, 3, 2, 6, 1], [5, 6, 2, 4],
                                        [3, 5, 2, -1, 4], [1], [2, 1, 4, 3, 6],
                                        [-1, -5, 2, 3], [-3, 2, -5, 6, -4]])
    print "test pre-processing pass"
    
testperp()

def solve_3SAT(num_variables, clauses, assignment = None):
    if assignment == None:
        assignment = [-1]*(num_variables+1)
        assignment[0] = 0
    clauses, assignment = sat_preprocessing(num_variables, clauses, assignment)
    if clauses == []:
        for i in range(0, len(assignment)):
            if assignment[i] == -1:
                assignment[i] = 0
        return assignment
    if clauses == [[1, -1]]:
        return None
    for i in range(1, len(assignment)):
        if assignment[i] == -1:
            assignment_pos = assignment[:]
            assignment_pos[i] = 1
            clauses_pos = deepcopy(clauses)
            clauses_pos = set_var(clauses_pos, i)
            pos = solve_3SAT(num_variables, clauses_pos, assignment_pos)
            #print 'pos', assignment_pos, pos
            assignment_neg = assignment[:]
            assignment_neg[i] = 0
            clauses_neg = deepcopy(clauses)
            clauses_neg = set_var(clauses_neg, -i)
            neg = solve_3SAT(num_variables, clauses_neg, assignment_neg)
            #print 'neg', assignment_neg, neg
            if neg != None:
                return neg
            elif pos != None:
                return pos
            else:
                return None
    return clauses, assignment


def test():
    clauses = [[-2, -3, -1], [3, -2, 1], [-3, 2, 1],
               [2, -3, -1], [3, -2, 1], [3, -2, 1]]
    solutions = [[0, 0, 0, 0],
                 [0, 0, 1, 1],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [1, 0, 0, 0],
                 [1, 0, 1, 1],
                 [1, 1, 0, 0],
                 [1, 1, 1, 0]]
    print solve_3SAT(3,clauses)
    assert solve_3SAT(3,clauses) in solutions

    clauses = [[2, 1, 3], [-2, -1, 3], [-2, 3, -1], [-2, -1, 3],
               [2, 3, 1], [-1, 3, -2], [-3, 2, 1], [1, -3, -2],
               [-2, -1, 3], [1, -2, -3], [-2, -1, 3], [-1, -2, -3],
               [3, -2, 1], [2, 1, 3], [-3, -1, 2], [-3, -2, 1],
               [-1, 3, -2], [1, 2, -3], [-3, -1, 2], [2, -1, 3]]
    assert solve_3SAT(3,clauses) == None

    clauses = [[-15, -4, 14], [-7, -4, 13], [-2, 18, 11], [-12, -11, -6], [7, 17, 4], [4, 6, 13], [-15, -9, -14], [14, -4, 8], [12, -5, -8], [6, -5, -2], [8, -9, 10], [-15, -11, -12], [12, 16, 17], [17, -9, -12], [-12, -4, 11], [-18, 17, -9], [-10, -12, -11], [-7, 15, 2], [2, 15, 17], [-15, -7, 10], [1, -15, 11], [-13, -1, -6], [-7, -11, 2], [-5, 1, 15], [-14, -13, 18], [14, 12, -1], [18, -16, 9], [5, -11, -13], [-6, 10, -16], [-2, 1, 4], [-4, -11, 8], [-8, 18, 1], [-2, 15, -13], [-15, -12, -10], [-18, -14, -6], [1, -17, 10], [10, -13, 2], [2, 17, -3], [14, 1, -17], [-16, -2, -11], [16, 7, 15], [-10, -6, 16], [4, -5, 10], [8, 10, -12], [1, -9, -14], [18, -9, 11], [16, 7, 12], [-5, -14, -13], [1, 18, 5], [11, 16, 5], [-8, 12, -2], [-6, -2, -13], [18, 16, 7], [-3, 9, -13], [-1, 3, 12], [-10, 7, 3], [-15, -6, -1], [-1, -7, -3], [1, 5, 13], [7, 6, -9], [1, -4, 3], [6, 8, 1], [12, 14, -8], [12, 5, -13], [-12, 15, 9], [-17, -8, 3], [17, -6, 8], [-3, -14, 4]]
    print solve_3SAT(18, clauses)
    print 'Tests passed'

test()
