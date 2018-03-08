#!/usr/bin/python
#
# run_reconstruction.py:
#
# run the databse reconstruction with the specified input file

SOLVER="picosat"

import sys
import subprocess

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

def latex_def(name,value):
    return "\\newcommand\\{}{{\\xspace{:,d}\\xspace}}\n".format(name,value)


sexmap = {"1":"M", "0":"F"}
rsexmap = reverse_map(sexmap)
racemap = {"1":"W", "0":"B"}
rracemap = reverse_map(racemap)
marriagemap = {"0":"S", "1":"M"}
rmarraigemap = reverse_map(marriagemap)

if __name__=="__main__":
    from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
    parser = ArgumentParser( formatter_class = ArgumentDefaultsHelpFormatter )
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--problem",default="one-block.csp")
    args = parser.parse_args()
    args.sugar_output = "constraints.sugar.out"
    args.sugar_cnf    = "constraints_.cnf"

    solver_with_seed="{} -s {} --all".format(SOLVER,args.seed)

    # Run the pre-processor and remove the files that begin with a '#'
    cmd = ['cpp',args.problem]
    (out,err) = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()
    with open("constraints.csp","w") as f:
        for line in out.decode('utf-8').split("\n"):
            if line.startswith('#'):
                continue
            f.write(line)
            f.write("\n")

    # Run sugar, which runs the solver
    cmd = ['perl','sugar-v2-3-2/bin/sugar',
           '-jar','sugar-v2-3-2/bin/sugar-v2-3-2.jar',
           '-solver',solver_with_seed,'-keep','-tmp','constraints_',
           '-output','constraints.out','constraints.csp']
    print(" ".join(cmd))
    r = subprocess.call(cmd,stdout=open(args.sugar_output,"w"))
    if r!=0:
        raise RuntimeError("sugar failed???")

    # Get the varaibles out of constraints.csp
    # Create the solved table

    cout = open(args.sugar_output,"r").read()
    if "ERROR" in cout:
        print("Error in running sugar:")
        print(cout)
        exit(1)
    

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

    for line in cout.split("\n"):
        line = line.strip()
        if len(line)==0: continue
        if line[0]=='s' and line!='s SATISFIABLE':
            raise RuntimeError("Constarints not satisfied")
        if line[0]=='a' and "\t" in line:
            (var,val) = line[2:].split("\t")
            vars[var] = val

    # Print information about reconstruction, sorted
    results = []
    for i in range(1,100):
        si = str(i)
        try:
            age=vars["A{}".format(i)]
        except KeyError:
            break
        desc = "{:>2}{}{}{}".format(age,
                                 sexmap[vars["S"+si]],
                                 racemap[vars["R"+si]],
                                 marriagemap[vars["M"+si]])
        results.append((int(age),desc))
    print("Seed: {}".format(args.seed))
    for (age,desc) in sorted(results):
        print(desc)
        
    # Now create the solved table
    with open("id_table.tex","r") as fin:
        with open("id_table_solved.tex","w") as fout:
            for line in fin:
                fout.write(" ".join([ unmap(var) for var in line.split(" ")]))
                    
    with open("vars.tex","w") as f:
        print(latex_def("NumConstraintLines",
                        linecount("constraints.csp",lambda a:";" not in a)),
              file=f)
        print(latex_def("NumSExpressions",
                        linecount("constraints.csp",lambda a:a.startswith("("))),
              file=f)
        (variables,clauses) = tally_dimacs_file(args.sugar_cnf)
        print(latex_def("NumVariables",variables),file=f)
        print(latex_def("NumClauses",clauses),file=f)
        print(latex_def("NumDIMACSLines", linecount(args.sugar_cnf,lambda a:True)),file=f)
