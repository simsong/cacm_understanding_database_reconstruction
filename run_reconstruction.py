#!/usr/bin/python
#
# run_reconstruction.py:
#
# run the databse reconstruction with the specified input file

SOLVER="picosat"

import sys
import re
from subprocess import Popen,PIPE,call
from collections import defaultdict
import time

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

def sugar_decode_picosat_out(outdata,mapfile):
    cmd = ['java','-cp',JARFILE,'jp.kobe_u.sugar.SugarMain','-decode','/dev/stdin',mapfile]
    print(" ".join(cmd))
    print("len(outdata)={}".format(len(outdata)))
    (out,err) = Popen(cmd,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate(outdata.encode('utf-8'))
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        raise RuntimeError("sugar decode error: "+err)
    return out

def extract_vars_from_sugar_decode(outdata):
    """Extract the variables from the sugar output. Returns a dictionary
    with the key the variable name and the value being the variable
    value"""
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

def sugar_decode_picostat_and_extract_vars(outdata,mapfile):
    return extract_vars_from_sugar_decode( sugar_decode_picosat_out( outdata, mapfile))

def python_decode_picostat_and_extract_vars(outdata,mapfile):
    vars    = {}                # extracted variables
    mapvars = {}
    with open(mapfile,"r") as f:
        for line in f:
            (var,name,start,_) = line.strip().split(" ")
            assert var=="int"
            (r0,r1) = _.split("..")
            start = int(start)
            r0 = int(r0)
            r1 = int(r1)
            mapvars[name] = (start,r0,r1)
    # Compute the highest possible variable
    highest = max(v[0]+v[2]-v[1] for v in mapvars.values())
    # Now read the boolean variables and map them back
    coefs = set()
    for line in lines_iter(outdata):
        if line[0]!='v': continue
        vals = [int(v) for v in line[2:].split(" ")]
        if abs(vals[0]) > highest:
            break               # no need to read any more
        coefs.update(vals)
    # Now for each variable, report its value
    for var in mapvars:
        (start,r0,r1) = mapvars[var]
        found = False
        for i in range(r1-r0):
            if start+i in coefs:
                vars[var] = str(r0+i)
                found = True
                break
        if not found:
            vars[var] = str(r0+1)
    return vars


def vars_to_codes(vars):
    """Transform the variables to a list of (age,code) person codes"""
    results = []
    ids = [int(k[1:]) for k in  vars.keys() if k[0]=='A'] # everybody has an age
    for i in ids:
        si  = str(i)
        print("si=",si)
        age = vars["A{}".format(i)]
        sex = vars["S"+si]
        race =vars["R"+si]
        marriage = vars["M"+si]
        print("sex=",sex)
        desc = "{:>2}{}{}{}".format(age, SEXMAP[sex], RACEMAP[race], MARRIAGEMAP[marriage])
        results.append((int(age),desc))
    return sorted(results)

def lines_iter(data):
    return (x.group(0) for x in re.finditer(".*", data) if x.group(0))

def parseall(data):
    picosat_out = ""
    total_solutions = 0
    solutions = 0
    seen = set()
    code_count = defaultdict(int)
    for line in lines_iter(data):
        if line.startswith('s'):
            if picosat_out:
                print("{}".format(total_solutions),end='')
                print("picosat_out = {} lines".format(picosat_out.count("\n")))
                sys.stdout.flush()
                vars = sugar_decode_picostat_and_extract_vars(picosat_out, args.map)
                print("vars=",vars)
                codes = parse_vars_to_printable(vars)
                print("codes=",codes)
                if codes not in seen:
                    solutions += 1
                    print("Solution:{}\n{}".format(solutions,codes))
                    seen.add(codes)
                    # Now add each code to the histogram
                    for (age,code) in vars_to_codes(vars):
                        code_count[code] += 1
                picosat_out = ''
        if line.startswith('s SOLUTIONS'):
            total_solutions = int(line.split(" ")[2])
            break
        picosat_out += line
    print("distinct solutions: {}  additional degenerate solutions: {}".
          format(solutions,total_solutions-solutions))
    for (key,value) in code_count.items():
        print("{} = {:3}".format(key,value))


            
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
    parser.add_argument("--decode",help="test the decode function")
    args = parser.parse_args()
    args.sugar_output = "constraints.sugar.out"

    def parse_vars_to_printable(out):
        ret = []
        for (age,code) in vars_to_codes(vars):
            ret.append(code)
            ret.append("\n")
        return "".join(ret)

    if args.parseout:
        out = open(args.parseout,"r").read()
        t0 = time.time()
        #vars = sugar_decode_picostat_and_extract_vars( out, args.map) 
        vars = python_decode_picostat_and_extract_vars( out, args.map) 
        print("vars:",vars)
        t1 = time.time()
        print(parse_vars_to_printable(out))
        print("time: {}".format(t1-t0))
        exit(1)

    if args.parseall:
        parseall(open(args.parseall,"r").read())
        exit(0)

    if args.decode:
        decode(open(args.decode,"r").read())
        exit(0)


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
           '-output','constraints.out']
    if args.all:
        cmd += ['-nodecode']

    cmd += ['constraints.csp']
    print(" ".join(cmd))
    t0 = time.time()
    p = Popen(cmd,stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate()
    t1 = time.time()
    sugar_out = out.decode('utf-8')
    sugar_err = err.decode('utf-8')
    if p.returncode!=0:
        raise RuntimeError("sugar returned {}. out='{}' err='{}'".format(p.returncode,sugar_out,sugar_err))
        exit(1)
    print("sugar run time: {:.4} sec".format(t1-t0))

    # keep a copy of the sugar output
    # Not strictly necessary, but useful for debugging
    with open(args.sugar_output,'w') as f:
        f.write(sugar_out)

    # Now constraints.out has the output from picosat

    if "ERROR" in sugar_out:
        print("Error in running sugar:")
        print(sugar_out)
        exit(1)
    
    if args.all:
        parseall(out)
        exit(0)

    vars    = extract_vars_from_sugar_decode(sugar_out)
    results = vars_to_codes(vars)

    # Print information about reconstruction, sorted
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
