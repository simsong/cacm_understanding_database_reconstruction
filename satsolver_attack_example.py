import pycosat
import itertools
import time
import dimacs_processor

# Program to simulate a Database Reconstruction Attack on databases
# of various sizes
# Uses pycosat - Python wrapper of the picoSAT SAT solver (in C)
# @author Christian Martindale

# EX:
# original CNF eqn is (A OR B) AND (NOT(B) OR C OR (NOT(D)))
# AND (D OR (NOT(E)))

#translated into DIMACS CNF format:

# p CNF 5 3
# 1 2 0
# -2 3 -4 0
# 4 -5 0

#pycosat input: List[List[int], ignore 0s
# myCNF = [[1,2], [-2,3,-4], [4,-5]]
#
# only yields the first solution found, if satisfiable
# ans = pycosat.solve(myCNF)
# yields as many solutions as it finds until iterator is exhausted
# allAns = pycosat.itersolve(myCNF)

FILE_NAME = "demo2.dimacs"

if __name__ == '__main__':
    input = dimacs_processor.process_dimacs(FILE_NAME)
    print("Solving for all solutions...")
    start_time = time.time()
    allAns = pycosat.itersolve(input)
    stop_time = time.time()
    time_elapsed = stop_time - start_time

    numAns = 0
    for solution in allAns:
        print("Solution: ", solution)
        numAns += 1
    if numAns == 0: print("Finished search in " , time_elapsed, ". System is unsatisfiable.")
    else: print("Number of solutions found in ", time_elapsed, "seconds" ": ", numAns)