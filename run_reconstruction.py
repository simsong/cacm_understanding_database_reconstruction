#!/usr/bin/python
#
# run_reconstruction.py:
#
# run the databse reconstruction with the specified input file

import os
import sys
import re
from subprocess import Popen,PIPE,call
from collections import defaultdict
import time

SUGAR_PERL = './sugar-v2-3-3/bin/sugar'
SUGAR_JAR  = './sugar-v2-3-3/bin/sugar-v2-3-3.jar'
# Our encodings
SEXMAP = {"1":"M", "0":"F"}
RACEMAP = {"1":"W", "0":"B"}
MARRIAGEMAP = {"0":"S", "1":"M"}

def is_cnf_file(fname):
    with open(fname,"r") as f:
        return f.read(6)=="p cnf "

def latex_def(name,value):
    return "\\newcommand\\{}{{\\xspace{:,d}\\xspace}}\n".format(name,value)

def lines_iter(data):
    """Returns the lines without a newline"""
    return (x.group(0) for x in re.finditer(".*", data) if x.group(0))

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

def sugar_encode_csp(*,cspfile,cnffile,mapfile):
    """Run sugar to make an output file"""
    assert os.path.exists(cspfile)
    assert not os.path.exists(cnffile)
    assert not os.path.exists(mapfile)
    cmd = ['java','-cp',SUGAR_JAR,'jp.kobe_u.sugar.SugarMain','-v', '-encode', cspfile, cnffile, mapfile]
    print(" ".join(cmd))
    p = Popen(cmd,stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate()
    sugar_out = out.decode('utf-8'); del out
    sugar_err = err.decode('utf-8'); del err
    if p.returncode!=0:
        raise RuntimeError("sugar returned {}. out='{}' err='{}'".format(p.returncode,sugar_out,sugar_err))
        exit(1)
    assert os.path.exists(cnffile)
    assert os.path.exists(mapfile)
    

def sugar_decode_picosat_out(outdata,mapfile):
    cmd = ['java','-cp',SUGAR_JAR,'jp.kobe_u.sugar.SugarMain','-decode','/dev/stdin',mapfile]
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

def sugar_decode_picostat_and_extract_vars(lines,mapfile):
    return extract_vars_from_sugar_decode( sugar_decode_picosat_out( "\n".join(lines), mapfile))

def get_mapvars(mapfile):
    """Read the sugar .map file and return a dictionary
    where the key is the variable name and the value is the (start,r0,r1)
    where r0 is the first ordinal and r1 is the last. Sugar uses uniary encoding."""
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
    return mapvars

def python_decode_picostat_and_extract_vars(lines,mapfile):
    """lines is an array of lines"""
    vars    = {}                # extracted variables
    mapvars = get_mapvars(mapfile)
    # Compute the highest possible variable
    highest = max(v[0]+v[2]-v[1] for v in mapvars.values())
    # Now read the boolean variables and map them back
    coefs = set()               # each variable is positive or negative
    for line in lines:
        # For each line in the DIMACS output file
        # read the numbers and add each to the coefficients set. 
        # stop when the first line is higher than the higest variable that we care about
        if line[0]!='v': continue
        vals = [int(v) for v in line[2:].split(" ")]
        if abs(vals[0]) > highest:
            break               # no need to read any more
        coefs.update(vals)

    # Now for each variable, check all of the booleans that make it up
    # to find the value of the variable. Also create the counter example.
    counter = set()
    for var in mapvars:
        (start,r0,r1) = mapvars[var]
        found = False           # we found the state change.
        for i in range(r1-r0):
            x = start+i
            if x in coefs:      # check for positive
                if not found:   # must be the transition from negative to positive
                    vars[var] = str(r0+i)
                    found = True
                coefs.add(-x)
            else:
                coefs.add(x)
        if not found:
            vars[var] = str(r0+1)
    return vars


def vars_to_codes(vars):
    """Transform the variables to a list of (age,code) person codes"""
    results = []
    ids = [int(k[1:]) for k in  vars.keys() if k[0]=='A'] # everybody has an age
    for i in ids:
        si  = str(i)
        age = vars["A{}".format(i)]
        sex = vars["S"+si]
        race =vars["R"+si]
        marriage = vars["M"+si]
        desc = "{:>2}{}{}{}".format(age, SEXMAP[sex], RACEMAP[race], MARRIAGEMAP[marriage])
        results.append((int(age),desc))
    return sorted(results)

def parse_vars_to_printable(vars):
    ret = []
    for (age,code) in vars_to_codes(vars):
        ret.append(code)
        ret.append("\n")
    return "".join(ret)

def parse_picosat_all_file(path):
    total_solutions = 0
    solutions = 0
    seen = set()
    code_count = defaultdict(int)
    ctr = 0
    picosat_out = []
    with open(path,"r") as f:
        for line in f:
            if line.startswith('s'):
                if picosat_out:
                    ctr += 1; print("{}\r".format(ctr),end='')
                    vars = python_decode_picostat_and_extract_vars(picosat_out, args.map)
                    codes = parse_vars_to_printable(vars)
                    if codes not in seen:
                        solutions += 1
                        print("Solution:{}\n{}".format(solutions,codes))
                        seen.add(codes)
                        # Now add each code to the histogram
                        for (age,code) in vars_to_codes(vars):
                            code_count[code] += 1
                    picosat_out = []
            if line.startswith('s SOLUTIONS'):
                total_solutions = int(line.split(" ")[2])
                break
            picosat_out.append(line)
    with open(args.all,"w") as f:
        print("distinct solutions: {}  additional degenerate solutions: {}".
              format(solutions,total_solutions-solutions))
        print(latex_def("NumDistinctSolutions",solutions),file=f)
        print(latex_def("DegenerateSolutions",total_solutions-solutions),file=f)
        for (key,value) in code_count.items():
            print("{} = {:3}".format(key,value))

def find_all_solutions(dimacsfile, mapfile):
    """Given a DIMACS file and a mapfile, solve the DIMACS file with a solver,
    then take the constraints (but only for the variables mentioned in the mapfile) 
    and find another solution"""

if __name__=="__main__":
    from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
    parser = ArgumentParser( formatter_class = ArgumentDefaultsHelpFormatter,
                             description="Runs sugar with picosat and parse the results into LaTeX")
    parser.add_argument("--problem",default="one-block.csp",help="specify the problem CSP")
    parser.add_argument("--cnf",default="constraints.cnf",help="specify cnf file")
    parser.add_argument("--parseout",
                        help="Parse the variables out of an .out file. A map file must be specified")
    parser.add_argument("--parseall",help='Evaluate output file of the picosat --all')
    parser.add_argument("--solver",default="picosat")
    parser.add_argument("--picosat_out",help='picosat output file',default='constraints.out')
    parser.add_argument("--map",help="Specify map file",default='constraints.map')
    parser.add_argument("--all",help="Compute all possible solutions; store results in ALL")
    parser.add_argument("--decode",help="test the decode function")
    parser.add_argument("--define",help="specify a #define to CPP")
    parser.add_argument("--sugar_output",help="specify sugar output",default='constraints.sugar.out')
    args = parser.parse_args()

    if args.parseout:
        out = open(args.parseout,"r").read()
        t0 = time.time()
        #vars = sugar_decode_picostat_and_extract_vars( out, args.map) 
        vars = python_decode_picostat_and_extract_vars( out, args.map) 
        t1 = time.time()
        print(parse_vars_to_printable(vars))
        print("time: {}".format(t1-t0))
        exit(1)

    if args.parseall:
        parse_picosat_all_file(args.parseall)
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
    solver_cmd=args.solver
    if args.all:
        solver_cmd += " --all"
    tmp = args.cnf.replace(".cnf","")

    # Here is what the Java looks like
    # java  -cp './sugar-v2-3-3/bin/sugar-v2-3-3.jar' jp.kobe_u.sugar.SugarMain -v -v  -encode 'constraints.csp' 'constraints.cnf' 'constraints.map'

    cmd = ['perl',SUGAR_PERL,
           '-jar',SUGAR_JAR,
           '-vv',
           '-solver',solver_cmd,'-keep','-tmp','constraints',
           '-output',args.picosat_out]
    if args.all:
        cmd += ['-nodecode']

    cmd += ['constraints.csp']
    print(" ".join(cmd))
    t0 = time.time()
    p = Popen(cmd,stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate()
    t1 = time.time()
    sugar_out = out.decode('utf-8'); del out
    sugar_err = err.decode('utf-8'); del err
    if p.returncode!=0:
        raise RuntimeError("sugar returned {}. out='{}' err='{}'".format(p.returncode,sugar_out,sugar_err))
        exit(1)
    print("sugar run time: {:.4} sec".format(t1-t0))

    if args.all:
        parse_picosat_all_file(args.picosat_out)
        exit(0)

    # keep a copy of the sugar output
    # Not strictly necessary, but useful for debugging
    with open(args.sugar_output,'w') as f:
        f.write(sugar_out)

    # Now constraints.out has the output from picosat

    if "ERROR" in sugar_out:
        print("Error in running sugar:")
        print(sugar_out)
        exit(1)
    
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
