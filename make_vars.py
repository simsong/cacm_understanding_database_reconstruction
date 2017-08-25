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
    # Get the varaibles out of constraints.csp
    # Create the solved table
    vars = {}
    with open("sugar.out","r") as f:
        for line in f:
            line = line.strip()
            if line[0]=='s' and line!='s SATISFIABLE':
                raise RuntimeError("Constarints not satisfied")
            if line[0]=='a' and "\t" in line:
                (var,val) = line[2:].split("\t")
                vars[var] = val

    with open("id_table.tex","r") as fin:
        with open("id_table_solved.tex","w") as fout:
            for line in fin:
                fout.write(" ".join([vars.get(var,var) for var in line.split(" ")]))
                    
    with open("vars.tex","w") as f:
        print("\\newcommand\\NumConstraintLines{{\\xspace{:,d}\\xspace}}".format(linecount("constraints.csp",lambda a:";" not in a)),file=f)
        print("\\newcommand\\NumSExpressions{{\\xspace{:,d}\\xspace}}".format(linecount("constraints.csp",lambda a:a.startswith("("))),file=f)
        (variables,clauses) = dimacs()
        print("\\newcommand\\NumVariables{{\\xspace{:,d}\\xspace}}".format(variables),file=f)
        print("\\newcommand\\NumClauses{{\\xspace{:,d}\\xspace}}".format(clauses),file=f)
        print("\\newcommand\\NumDIMACSLines{{\\xspace{:,d}\\xspace}}".format(linecount("constraints_.cnf",lambda a:True)),file=f)

        
