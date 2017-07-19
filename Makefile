all:
	latexmk -pdf white_paper.tex

clean:
	latexmk -c -C 
	/bin/rm -f *.bbl *.fls *~ *.spl


