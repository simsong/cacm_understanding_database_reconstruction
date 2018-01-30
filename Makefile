SOLVER=Walksat_v51/walksat
SOLVER=picosat

white_paper.pdf: vars.tex white_paper.tex 
	latexmk -pdf white_paper.tex

solve:	constraints.sugar.out

constraints.sugar.out: constraints.csp  Makefile
	perl sugar-v2-3-2/bin/sugar -jar sugar-v2-3-2/bin/sugar-v2-3-2.jar -solver $(SOLVER) -keep -tmp constraints_ -output constraints.out constraints.csp > constraints.sugar.out

vars.tex: make_vars.py constraints.sugar.out
	python make_vars.py  constraints.sugar.out

clean:
	latexmk -c -C 
	/bin/rm -f *.bbl *.fls *~ *.spl



