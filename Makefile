all: vars.tex constraints_.cnf
	latexmk -pdf white_paper.tex

constraints_.cnf: constraints.csp 
	perl sugar-v2-3-2/bin/sugar -jar sugar-v2-3-2/bin/sugar-v2-3-2.jar \
	     -keep -tmp constraints_ -output constraints.out constraints.csp > sugar.out
	diff sugar.out sugar.out.good

vars.tex: constraints_.cnf make_vars.py
	python make_vars.py 

clean:
	latexmk -c -C 
	/bin/rm -f *.bbl *.fls *~ *.spl



