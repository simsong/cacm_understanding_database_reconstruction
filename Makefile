#
# We have two reconstructions:
# two-households.csp 11 people
# one-block.csp       7 people, with medians

SOLVER="picosat -s 3"
PROBLEM=one-block.csp

all: white_paper.pdf toy_mechanism.pdf

white_paper.pdf: vars.tex white_paper.tex medians.tex
	latexmk -pdf white_paper.tex </dev/null

toy: toy_mechanism.pdf
toy_mechanism.pdf: toy_mechanism.tex toy_regression.pdf
	latexmk -pdf toy_mechanism.tex </dev/null

toy_regression.pdf: toy_regression.py
	python3 toy_regression.py

solve:	constraints.sugar.out

vars.tex: make_vars.py constraints.sugar.out id_table.tex
	python make_vars.py  constraints.sugar.out constraints_.cnf

medians.tex: median_calculator.py tytable.py
	python median_calculator.py

constraints.sugar.out: constraints.csp  Makefile 
	perl sugar-v2-3-2/bin/sugar -jar sugar-v2-3-2/bin/sugar-v2-3-2.jar \
             -solver $(SOLVER) -keep -tmp constraints_ \
             -output constraints.out constraints.csp > constraints.sugar.out
	@if grep ERROR constraints.sugar.out >/dev/null ; then \
	     echo ========= ERROR ============ ; \
	     cat constraints.sugar.out ; exit 1; \
	     fi

constraints.csp: $(PROBLEM)
	cpp $(PROBLEM) | sed 's/^#/;/' > constraints.csp

clean:
	latexmk -c -C 
	/bin/rm -f *.bbl *.fls *~ *.spl
	/bin/rm -f vars.tex


