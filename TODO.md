Suggested sources to check out:

- http://ssa-school-2016.it.uu.se/wp-content/uploads/2016/06/jpms-satsmtar16-slides.pdf

- http://ssa-school-2016.it.uu.se/wp-content/uploads/2016/06/LaurentSimon.pdf

- http://satsmt2014.forsyte.at/files/2014/07/SAT-introduction.pdf


Best-known generic SAT-solver today: CDCL. Many (all?) implementations of CDCL  that are out there (e.g. google: CDCL + github) would do just fine. CDCL is the state-of-the-art for generic problems, i.e. if you don't know much about its structure this is more or less the way to go. 

Best implementation of CDCL: Lingeling 


Suggested another solver: Glucose

There are also "educational" versions of CDCL solvers: Laurent Simon coded up
one in Python for his tutorial in 2016 (linked to above) and Armin
Biere made a version Cleaneling for a tutorial some previous year.

3. SMT: CDCL + lazy-SMT. I am not aware of any free to download implementations of this, but your best best is to use one of the uses of a CDCL sat-solver for embedding SMT problems. The best way to do this in practice is called lazy-SMT. I am not an expert in this. Here is an implementation I found by a google search right now:  https://github.com/mihaidusmanu/MSMTS 


In general, the generic way to use a CDCL solver together as a lazy-SMT solver is described in a 10-year-old paper: http://dl.acm.org/citation.cfm?id=1217859 

Notes from a colleague on SAT vs. linear solvers:

"4. Yes, I did see (back in the days) a few works doing what you are suggesting. In my opinion, this is not a worthy enterprise. The other direction, using Gurobi to solve SAT is the correct way to go. Keep in mind that academic SAT-solvers cannot seriously compete with commercial MIP solvers, on generic problems. One reason is that the optimization community is around for much longer than sat-solvers (longer than computer science as a whole if you like). Furthermore, compared to sat-solving there are much more people that do MIP. Gurobi (and CPLEX) are commercial products. To conclude: if you are planning to get engaged in a longer-term research project then my suggestion is to (1) spend time learning about sat-solvers, (2) come up with a heuristic related to the specific problem you want to solve and add this heuristic to your favorite implementation of CDCL (they are usually quite scalable), and (3) verify that runs much better than the encoding of your problem as an integer program when solved by e.g. Gurobi. But, if you aim to just use a solver once or twice then I'd recommend you use one of the commercial MIP optimization packages."


