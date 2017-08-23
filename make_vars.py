#!/usr/bin/python

def linecount(fname,filter_func):
    return len(list(filter(filter_func,open(fname,"r").read().split("\n"))))

def dimacs():
    with open("constraints_.cnf","r") as f:
        for line in f:
            if line[0]=='c': continue
            fields = line.strip().split(" ")
            assert fields[0]=='p'
            assert fields[1]=='cnf'
            return (int(fields[2]),int(fields[3]))
            

if __name__=="__main__":
    with open("vars.tex","w") as f:
        print("\\newcommand\\NumConstraintLines{{ {} }}".format(linecount("constraints.csp",lambda a:";" not in a)),file=f)
        print("\\newcommand\\NumSExpressions{{ {} }}".format(linecount("constraints.csp",lambda a:a.startswith("("))),file=f)
        (variables,clauses) = dimacs()
        print("\\newcommand\\NumVariables{{ {} }}".format(variables),file=f)
        print("\\newcommand\\NumClauses{{ {:,d} }}".format(clauses),file=f)
        print("\\newcommand\\NumDIMACSLines{{ {:,d} }}".format(linecount("constraints_.cnf",lambda a:True)),file=f)

