#!/usr/bin/python

# Test the reconstruction

from run_reconstruction import *

import os
import contextlib

CSP=""";; a simple CSP to test factoring
;; find all factors of 15

(int X1 0 100)
(int Y1 0 100)
(= (* X1 Y1) 15)
"""

MAP="""int X1 1 1..100
int Y1 100 0..100
"""

CSP_FILE="tests/factor.csp"
MAP_FILE="tests/factor.map"
CNF_FILE="tests/factor.cnf"
OUT_FILE="tests/factor.out"

def test_sugar_encode_csp():
    with contextlib.suppress(FileNotFoundError):
        os.remove(CSP_FILE)
    with open(CSP_FILE,"w") as f:
        f.write(CSP)
    with contextlib.suppress(FileNotFoundError):
        os.remove(MAP_FILE)
    with contextlib.suppress(FileNotFoundError):
        os.remove(CNF_FILE)
    sugar_encode_csp(cspfile=CSP_FILE,mapfile=MAP_FILE,cnffile=CNF_FILE)
    assert os.path.exists(MAP_FILE)
    assert os.path.exists(CNF_FILE)
    with open(MAP_FILE,"r") as f:
        assert f.read()==MAP
    assert is_cnf_file(CNF_FILE)
    
def test_run_solver():
    with contextlib.suppress(FileNotFoundError):
        os.remove(OUT_FILE)
    run_solver(solver=DEFAULT_SOLVER,cnffile=CNF_FILE,outfile=OUT_FILE)

def test_decode_vars():
    assert os.path.exists(MAP_FILE)
    assert os.path.exists(OUT_FILE)
    mapvars = get_mapvars(MAP_FILE)
    assert "X1" in mapvars
    assert "Y1" in mapvars
    assert mapvars["X1"]==(1,1,100)
    assert mapvars["Y1"]==(100,0,100)
    
CONSTRAINTS1 = {'S1': '0', 'S2': '1', 'S3': '0', 'S4': '1', 'S5': '0', 'S6': '0', 'S7': '1', 'A1': '8', 'A2': '18', 'A3': '24', 'A4': '30', 'A5': '36', 'A6': '66', 'A7': '84', 'R1': '0', 'R2': '1', 'R3': '1', 'R4': '1', 'R5': '0', 'R6': '0', 'R7': '0', 'M1': '0', 'M2': '0', 'M3': '0', 'M4': '1', 'M5': '1', 'M6': '1', 'M7': '1', 'FEMALE_ID1': '1', 'FEMALE_ID2': '3', 'FEMALE_ID3': '5', 'FEMALE_ID4': '6', 'FEMALE_AGE1': '8', 'FEMALE_AGE2': '24', 'FEMALE_AGE3': '36', 'FEMALE_AGE4': '66', 'MALE_ID1': '2', 'MALE_ID2': '4', 'MALE_ID3': '7', 'MALE_AGE1': '18', 'MALE_AGE2': '30', 'MALE_AGE3': '84', 'BLACK_ID1': '1', 'BLACK_ID2': '5', 'BLACK_ID3': '6', 'BLACK_ID4': '7', 'BLACK_AGE1': '8', 'BLACK_AGE2': '36', 'BLACK_AGE3': '66', 'BLACK_AGE4': '84', 'WHITE_ID1': '2', 'WHITE_ID2': '3', 'WHITE_ID3': '4', 'WHITE_AGE1': '18', 'WHITE_AGE2': '24', 'WHITE_AGE3': '30'}

def test_sugar_decode_picostat_and_extract_satvars():
    lines   = open("tests/constraints1.out","r").read().split("\n")
    mapfile = "tests/constraints1.map"
    satvars = sugar_decode_picostat_and_extract_satvars(lines,mapfile)
    assert satvars == CONSTRAINTS1

def test_extract_vars_from_solver_output():
    lines   = open("tests/constraints1.out","r").read().split("\n")
    mapfile = "tests/constraints1.map"
    (mapvars,satvars,counter) = extract_vars_from_solver_output(solver_output_lines=lines,mapfile=mapfile)
    print("CONSTRAINTS1=",CONSTRAINTS1)
    print("satvars2=",satvars)
    assert satvars == CONSTRAINTS1

if __name__=="__main__":
    test_sugar_decode_picostat_and_extract_satvars()
    test_extract_vars_from_solver_output()
