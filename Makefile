#
# We have two reconstructions:
# two-households.csp 11 people
# one-block.csp       7 people, with medians

all: white_paper.pdf toy_mechanism.pdf

white_paper.pdf: vars.tex white_paper.tex medians.tex
	latexmk -pdf white_paper.tex </dev/null

toy: toy_mechanism.pdf
toy_mechanism.pdf: toy_mechanism.tex toy_regression.pdf
	latexmk -pdf toy_mechanism.tex </dev/null

toy_regression.pdf: toy_regression.py
	python3 toy_regression.py

solve:	constraints.sugar.out

vars.tex: run_reconstruction.py constraints.csp
	python run_reconstruction.py

medians.tex: median_calculator.py tytable.py
	python median_calculator.py

constraints.csp: $(PROBLEM)
	cpp $(PROBLEM) | sed 's/^#/;/' > constraints.csp

clean:
	latexmk -c -C 
	/bin/rm -f *.bbl *.fls *~ *.spl
	/bin/rm -f vars.tex


