#!/usr/bin/python
#
# run_reconstruction.py:
#
# run the databse reconstruction with the specified input file

SOLVER="picosat"

import sys
from subprocess import Popen,PIPE,call

JARFILE='./sugar-v2-3-2/bin/sugar-v2-3-2.jar'
# Our encodings
SEXMAP = {"1":"M", "0":"F"}
RACEMAP = {"1":"W", "0":"B"}
MARRIAGEMAP = {"0":"S", "1":"M"}

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

def unmap(var):
    # Given a variable that is to be unmapped (e.g. A2)
    # transform it to text
    try:
        rvar = vars[var]        # rvar is what we are returning
    except KeyError:
        return var
    if var[0]=='S':
        return SEXMAP[rvar]
    if var[0]=='R':
        return RACEMAP[rvar]
    if var[0]=='M':
        return MARRIAGEMAP[rvar]
    # Must be an age
    return rvar

def latex_def(name,value):
    return "\\newcommand\\{}{{\\xspace{:,d}\\xspace}}\n".format(name,value)

def decode_picosat_out(outdata,mapfile):
    cmd = ['java','-cp',JARFILE,'jp.kobe_u.sugar.SugarMain','-decode','/dev/stdin',mapfile]
    (out,err) = Popen(cmd,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate(outdata.encode('utf-8'))
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        raise RuntimeError("sugar decode error: "+err)
    return out

def extract_vars(outdata):
    """Extract the variables from the sugar output."""
    # vars[] is the mapping of the sugar variable to the solution
    vars = {}

    for line in outdata.split("\n"):
        line = line.strip()
        if len(line)==0: continue
        if line[0]=='s' and line!='s SATISFIABLE':
            raise RuntimeError("Constraints not satisfied")
        if line[0]=='a' and "\t" in line:
            (var,val) = line[2:].split("\t")
            vars[var] = val
    return vars

def vars_to_codes(vars):
    """Transform the variables to a list of (age,code) person codes"""
    results = []
    for i in range(1,100):
        si = str(i)
        try:
            age=vars["A{}".format(i)]
        except KeyError:
            break
        desc = "{:>2}{}{}{}".format(age,
                                 SEXMAP[vars["S"+si]],
                                 RACEMAP[vars["R"+si]],
                                 MARRIAGEMAP[vars["M"+si]])
        results.append((int(age),desc))
    results.sort()
    return results

if __name__=="__main__":
    from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
    parser = ArgumentParser( formatter_class = ArgumentDefaultsHelpFormatter,
                             description="Runs sugar with picosat and parse the results into LaTeX")
    parser.add_argument("--seed",type=int,default=0,help="specify the seed for the solver")
    parser.add_argument("--problem",default="one-block.csp",help="specify the problem CSP")
    parser.add_argument("--cnf",default="constraints.cnf",help="specify cnf file")
    parser.add_argument("--parseout",help="Parse the variables out of an .out file. A map file must be specified")
    parser.add_argument("--parseall",help='Evaluate output file of the picosat --all')
    parser.add_argument("--out",help='sugar output file',default='constraints.out')
    parser.add_argument("--map",help="Specify map file",default='constraints.map')
    parser.add_argument("--all",help="Compute all possible solutions",action="store_true")
    args = parser.parse_args()
    args.sugar_output = "constraints.sugar.out"

    def parse_and_print(out):
        res = decode_picosat_out(out,args.map)
        vars = extract_vars(res)
        for (age,code) in sorted(vars_to_codes(vars)):
            print(code)

    if args.parseout:
        out = open(args.parseout,"r").read()
        parse_and_print(out)
        exit(1)

    if args.parseall:
        out = ""
        solutions = 0
        for line in open(args.parseall,"r"):
            if line.startswith('s'):
                if out:
                    solutions += 1
                    print("Solution:{}  out(lines)={}".format(solutions,out.count("\n")))
                    print("out first line: {}".format(out.split("\n")[0]))
                    print("out last line: {}".format(out.split("\n")[-1]))
                    parse_and_print(out)
                    out = ''
            if line.startswith('s SOLUTIONS'):
                print("line=",line)
                assert str(solutions) in line
                break
            out += line
        exit(1)
        

    # Run the pre-processor and remove the files that begin with a '#'
    cmd = ['cpp',args.problem]
    (out,err) = Popen(cmd,stdout=PIPE).communicate()
    with open("constraints.csp","w") as f:
        for line in out.decode('utf-8').split("\n"):
            if line.startswith('#'):
                continue
            f.write(line)
            f.write("\n")

    # Run sugar, which runs the solver
    all = "" if not args.all else " --all"
    solver_cmd="{} -s {}{}".format(SOLVER,args.seed,all)
    tmp = args.cnf.replace(".cnf","")
    cmd = ['perl','sugar-v2-3-2/bin/sugar',
           '-jar','sugar-v2-3-2/bin/sugar-v2-3-2.jar',
           '-solver',solver_cmd,'-keep','-tmp','constraints',
           '-output','constraints.out','constraints.csp']
    print(" ".join(cmd))
    p = Popen(cmd,stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate()
    sugar_out = out.decode('utf-8')
    sugar_err = err.decode('utf-8')
    if p.returncode!=0:
        raise RuntimeError("sugar returned {}. out='{}' err='{}'".format(p.returncode,sugar_out,sugar_err))
        exit(1)

    # keep a copy of the sugar output
    # Not strictly necessary, but useful for debugging
    with open(args.sugar_output,'w') as f:
        f.write(sugar_out)

    # Now constraints.out has the output from picosat
    # args.sugar_output has the output from sugar

    if "ERROR" in sugar_out:
        print("Error in running sugar:")
        print(sugar_out)
        exit(1)
    
    vars    = extract_vars(sugar_out)
    results = vars_to_codes(vars)

    # Print information about reconstruction, sorted
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
        (variables,clauses) = tally_dimacs_file(args.cnf)
        print(latex_def("NumVariables",variables),file=f)
        print(latex_def("NumClauses",clauses),file=f)
        print(latex_def("NumDIMACSLines", linecount(args.cnf,lambda a:True)),file=f)
