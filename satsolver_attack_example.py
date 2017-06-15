import pycosat
import itertools
import dimacs_processor

# Program to simulate a Database Reconstruction Attack on databases
# of various sizes
# Uses pycosat - Python wrapper of the picoSAT SAT solver (in C)
# @author Christian Martindale

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
# print("First solution found: " , ans)
# print("All solutions found: ")
# for solution in allAns:
#     print(solution)
# print("Total number of solutions: " , len(list(pycosat.itersolve(myCNF))))

FILE_NAME = "demo1.dimacs"

if __name__ == '__main__':
    input = dimacs_processor.process_dimacs(FILE_NAME)
