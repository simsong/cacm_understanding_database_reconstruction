#!/usr/bin/python

def linecount(fname,filter_func):
    return len(list(filter(filter_func,open(fname,"r").read().split("\n"))))

def tally_dimacs_file(dimacs_file):
    with open(dimacs_file,"r") as f:
        for line in f:
            if line[0]=='c': continue
            fields = line.strip().split(" ")
            assert fields[0]=='p'
            assert fields[1]=='cnf'
            return (int(fields[2]),int(fields[3]))
            

def reverse_map(m):
    return {v: k for k, v in m.items()}

sexmap = {"1":"M", "0":"F"}
rsexmap = reverse_map(sexmap)
racemap = {"1":"W", "0":"B"}
rracemap = reverse_map(racemap)
marriagemap = {"0":"S", "1":"M"}
rmarraigemap = reverse_map(marriagemap)

if __name__=="__main__":
    from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(
        formatter_class = ArgumentDefaultsHelpFormatter)

    parser.add_argument("sugar_output",help="Sugar file standard output")
    parser.add_argument("sugar_cnf",help="Sugar cnf file")
    args = parser.parse_args()
    # Get the varaibles out of constraints.csp
    # Create the solved table
    import sys
    
    # vars[] is the mapping of the sugar variable to the solution
    vars = {}
    def unmap(var):
        # Given a variable that is to be unmapped (e.g. A2)
        # transform it to text
        try:
            rvar = vars[var]        # rvar is what we are returning
        except KeyError:
            return var
        if var[0]=='S':
            return sexmap[rvar]
        if var[0]=='R':
            return racemap[rvar]
        if var[0]=='M':
            return marriagemap[rvar]
        # Must be an age
        return rvar

    with open(args.sugar_output,"r") as f:
        for line in f:
            line = line.strip()
            if line[0]=='s' and line!='s SATISFIABLE':
                raise RuntimeError("Constarints not satisfied")
            if line[0]=='a' and "\t" in line:
                (var,val) = line[2:].split("\t")
                vars[var] = val

    # Print classified advertisements
    for i in range(1,100):
        si = str(i)
        try:
            age=vars["A{}".format(i)]
        except KeyError:
            break
        print("{}{}{}{}".format(marriagemap[vars["M"+si]],
                                racemap[vars["R"+si]],
                                sexmap[vars["S"+si]],
                                age))
        
    # Now create the solved table
    with open("id_table.tex","r") as fin:
        with open("id_table_solved.tex","w") as fout:
            for line in fin:
                fout.write(" ".join([ unmap(var) for var in line.split(" ")]))
                    
    with open("vars.tex","w") as f:
        print("\\newcommand\\NumConstraintLines{{\\xspace{:,d}\\xspace}}"
              .format(linecount("constraints.csp",lambda a:";" not in a)),file=f)
        print("\\newcommand\\NumSExpressions{{\\xspace{:,d}\\xspace}}"
              .format(linecount("constraints.csp",lambda a:a.startswith("("))),file=f)
        (variables,clauses) = tally_dimacs_file(args.sugar_cnf)
        print("\\newcommand\\NumVariables{{\\xspace{:,d}\\xspace}}"
              .format(variables),file=f)
        print("\\newcommand\\NumClauses{{\\xspace{:,d}\\xspace}}"
              .format(clauses),file=f)
        print("\\newcommand\\NumDIMACSLines{{\\xspace{:,d}\\xspace}}"
              .format(linecount("constraints_.cnf",lambda a:True)),file=f)

        
