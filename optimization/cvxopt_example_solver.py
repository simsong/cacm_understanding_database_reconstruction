import cvxpy as cp
import numpy as np

# goal is to solve the problem in example_survey_responses.txt with an optimizer
# define a new fxn for every constraint, then add them all up for the obj function? (each sub function returns
# 1 if met and -1000 if not met)

objective = cp.Maximize(constraint_sum_fxn)

master_constraints = []

def constraint_sum_fxn:


A = cp.Int(10)
H = cp.Int(10)
S = cp.Int(10)
R = cp.Int(10)
G = cp.Int(10)

bounds = []

bounds.append(A[0] >= 10)
bounds.append(A[0] <= 90)
bounds.append(A[1] >= 10)
bounds.append(A[1] <= 90)
bounds.append(A[2] >= 10)
bounds.append(A[2] <= 90)
bounds.append(A[3] >= 10)
bounds.append(A[3] <= 90)
bounds.append(A[4] >= 10)
bounds.append(A[4] <= 90)
bounds.append(A[5] >= 10)
bounds.append(A[5] <= 90)
bounds.append(A[6] >= 10)
bounds.append(A[6] <= 90)
bounds.append(A[7] >= 10)
bounds.append(A[7] <= 90)
bounds.append(A[8] >= 10)
bounds.append(A[8] <= 90)
bounds.append(A[9] >= 10)
bounds.append(A[9] <= 90)

bounds.append(H[0] >= 1)
bounds.append(H[0] <= 2)
bounds.append(H[1] >= 1)
bounds.append(H[1] <= 2)
bounds.append(H[2] >= 1)
bounds.append(H[2] <= 2)
bounds.append(H[3] >= 1)
bounds.append(H[3] <= 2)
bounds.append(H[4] >= 1)
bounds.append(H[4] <= 2)
bounds.append(H[5] >= 1)
bounds.append(H[5] <= 2)
bounds.append(H[6] >= 1)
bounds.append(H[6] <= 2)
bounds.append(H[7] >= 1)
bounds.append(H[7] <= 2)
bounds.append(H[8] >= 1)
bounds.append(H[8] <= 2)
bounds.append(H[9] >= 1)
bounds.append(H[9] <= 2)


master_constraints += bounds
