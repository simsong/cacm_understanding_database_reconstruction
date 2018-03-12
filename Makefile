#
# We have two reconstructions:
# two-households.csp 11 people
# one-block.csp       7 people, with medians

PROBLEM=one-block.csp
all: white_paper.pdf toy_mechanism.pdf

white_paper.pdf: vars.tex white_paper.tex medians.tex
	latexmk -pdf white_paper.tex </dev/null

toy: toy_mechanism.pdf
toy_mechanism.pdf: toy_mechanism.tex toy_regression.pdf
	latexmk -pdf toy_mechanism.tex </dev/null

toy_regression.pdf: toy_regression.py
	python3 toy_regression.py

vars.tex: run_reconstruction.py $(PROBLEM)
	python run_reconstruction.py

medians.tex: median_calculator.py tytable.py
	python median_calculator.py

clean:
	latexmk -c -C 
	/bin/rm -f *.bbl *.fls *~ *.spl
	/bin/rm -f constraints.sugar.out vars.tex medians.tex toy_mechanism.pdf



