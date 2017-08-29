The purpose of this project is to teach data agency officials about the dangers
of database reconstruction attacks. 

The problem statement and white paper are found in [problem_analysis.md](problem_analysis.md).

`.dimacs` files contain [CNF](https://en.wikipedia.org/wiki/Conjunctive_normal_form) files to feed into the demo solver in the DIMACS file format.

Demo program using pycoSAT can be found in satsolver_attack_example.py.
  
[pycosat SAT Solver Information/Download](https://pypi.python.org/pypi/pycosat)

[Naoyuki Tamura](http://bach.istc.kobe-u.ac.jp/tamura.html) [research](http://bach.istc.kobe-u.ac.jp/research.html):
* [Sugar](http://bach.istc.kobe-u.ac.jp/sugar/)


# To Do:

* Create the output table automatically from the sugar output

1. I made some minor changes (typos, sentence restructuring, and explaining a term or two)
2. You seem to have removed the table with the ground truth responses to the survey, and only give the statistics generated from these responses. As a result, we can’t demonstrate that the Sugar output matches the original responses, since the reader never sees the original responses. The table reference in the section discussing the Sugar output is also returning ?? because it refers to the ground truth table that was removed
3. Do we need to explain what we mean by “3SAT”, or are we assuming the audience knows?
4. You talk in the introduction about how formally proving privacy is important instead of relying on “hunches", but then we never revisit that topic in the section where we actually add the noise and rerun Sugar. I’m not sure if the way I added noise from the Laplace mechanism was differentially private or not. I think we should either remove the parts about formal privacy from the intro or add an explanation in the last section about how we can now say that our database is mathematically sound against a DRA.