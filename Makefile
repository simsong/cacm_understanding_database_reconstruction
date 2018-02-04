SOLVER=picosat
PROBLEM=one-block.csp

white_paper.pdf: vars.tex white_paper.tex 
	latexmk -pdf white_paper.tex </dev/null

toy_mechanism.pdf: toy_mechanism.tex toy_regression.pdf
	latexmk -pdf toy_mechanism.tex </dev/null

toy_regression.pdf: toy_regression.py
	python3 toy_regression.py

solve:	constraints.sugar.out

vars.tex: make_vars.py constraints.sugar.out
	python make_vars.py  constraints.sugar.out constraints_.cnf

constraints.sugar.out: constraints.csp  Makefile
	perl sugar-v2-3-2/bin/sugar -jar sugar-v2-3-2/bin/sugar-v2-3-2.jar \
             -solver $(SOLVER) -keep -tmp constraints_ \
             -output constraints.out $(PROBLEM) > constraints.sugar.out

clean:
	latexmk -c -C 
	/bin/rm -f *.bbl *.fls *~ *.spl



