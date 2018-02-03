# Sat solvers:
https://cstheory.stackexchange.com/posts/7473/revisions
# 

The purpose of this project is to teach data agency officials about
the dangers of database reconstruction attacks.

The problem statement and white paper are found in
[problem_analysis.md](problem_analysis.md).

`.dimacs` files contain [CNF](https://en.wikipedia.org/wiki/Conjunctive_normal_form) files to feed into the demo solver in the DIMACS file format.

Demo program using pycoSAT can be found in satsolver_attack_example.py.
  
We evaluated three SAT solvers:
* picosat
* minisat
* Walksat_v51

We found that picosat reliably worked best, running in the fastest time and with the least amount of memory.  Minisat was always slower, Walksat did not find solutions.

Input for the SAT solver was created with [Naoyuki Tamura](http://bach.istc.kobe-u.ac.jp/tamura.html) [research](http://bach.istc.kobe-u.ac.jp/research.html)'s Sugar program:

* [Sugar](http://bach.istc.kobe-u.ac.jp/sugar/)


4. You talk in the introduction about how formally proving privacy is important instead of relying on “hunches", but then we never revisit that topic in the section where we actually add the noise and rerun Sugar. I’m not sure if the way I added noise from the Laplace mechanism was differentially private or not. I think we should either remove the parts about formal privacy from the intro or add an explanation in the last section about how we can now say that our database is mathematically sound against a DRA.