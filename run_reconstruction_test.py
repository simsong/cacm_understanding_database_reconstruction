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
    
    
