import numpy as np
from pulp import LpVariable, LpProblem, LpMaximize, LpStatus, value

def varName(i,j):
    return "x_" + str(i) + "," + str(j)

def solutionDict(problem):
    _sol = {}
    for v in problem.variables():
        _sol[v.name] = v.varValue
    return _sol

def addHardConst(problem, i, j):
    solution = solutionDict(problem)
    prevVal = solution[varName(i,j)]
    print "Hard reviewing cosntraint (" + str(i) + ", " + str(j) + ")"

    problem += lpVars[i][j] == abs(prevVal - 1), "Hard reviewing cosntraint (" + str(i) + ", " + str(j) + ")"
    return problem

def numDiffs(sol1, sol2):
    count = 0
    for (variable, val) in sol1.iteritems():
        if sol2[variable] != val:
            count += 1
    return count

# parameters
nRev = 10
nPap = 25
alpha = 5
beta = 2

# weights
weights = np.random.rand(nRev, nPap)

# LP instance
prob = LpProblem("b-Matching", LpMaximize)

# primal variables
lpVars = []
for i in range(nRev):
    lpVars.append([])
    for j in range(nPap):
        lpVars[i].append(LpVariable(varName(i,j), 0, 1))

prob += sum([ weights[i][j] * lpVars[i][j] for i in range(nRev) for j in range(nPap) ]), "total affinity"

# reviewer constraints
for r in range(nRev):
    prob += sum(lpVars[r]) <= alpha, "reviewer " + str(r) + " cannot review more than " + str(alpha) + " papers"

# paper constraints
for p in range(nPap):
    prob += sum([ lpVars[i][p] for i in range(nRev) ]) >= beta, "paper " + str(p) + " must be reviewed at least " + str(beta) + " times"

prob.solve()

#for v in prob.variables():
#    print v.name, "=", v.varValue
#print "Total affinity = ", prob.objective

# initialize with first solution
prob.solve()
init = {}
for v in prob.variables():
    init[v.name] = v.varValue

sol1 = init
nConsts = 12
pairs = [ (i,j) for i in range(nRev) for j in range(nPap) ]
arbitraryConsts = np.random.choice(len(pairs), nConsts, replace=False)
print arbitraryConsts

for i in range(0,12,3):
    (next_i, next_j) = pairs[arbitraryConsts[i]]
    prob = addHardConst(prob, next_i, next_j)
    (next_i, next_j) = pairs[arbitraryConsts[i+1]]
    prob = addHardConst(prob, next_i, next_j)
    (next_i, next_j) = pairs[arbitraryConsts[i+2]]
    prob = addHardConst(prob, next_i, next_j)
    prob.solve()
    print "Status:", LpStatus[prob.status]
    print "Total affinity = ", value(prob.objective)
    sol2 = {}
    for v in prob.variables():
        sol2[v.name] = v.varValue
    print "Num Diffs:", numDiffs(sol1,sol2)
    for (variable, val) in sol2.iteritems():
        sol1[variable] = val
