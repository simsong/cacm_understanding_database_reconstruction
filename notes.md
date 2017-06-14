# Project Goals and Deliverables:

Project type:  Educational project
Key hurdles to overcome: 
     - Writing something readalbe; 
     - developing a clean exmaple; 
     - use open source solvers to solve a problem too hard to solve by hand.

Audience:
  * Census managers & thought leaders
  * Users of Census data products (later on)


1. A paper that demonstrates the fesability of a database reconstruction attack against the products of a statistical agency:
  
- Using a toy example that makes sense to a person with high-school level math background.

- Showing that complex constraint systems can be solved with modern tools very quickly.

  --- To do this, we will probably need to show that the example with a small number (10?) of people can be scaled up to a larger number of people (100?) with minimal increase in runtime.


2. Establish a English vocabulary for discussion of the risks of database reconstruction. 

   "database reconstruction"
   "risk"
   "universe of possible reconstructions"

   (these are probably the wrong words.)

3. Show solution of noise infusion.
   - Show that when we add noise, some statistics don't degrade much, but reconstruction becomes probabalistic.

   - Show the accuracy/privacy tradeoff.

4. (optional?) Show why traditional disclosure avoidance techniques don't work.

   - Cell suppression.

================================================================

tools that I used:

1. Installed picosat.
2. Installed Naoyuki Tamura's [http://bach.istc.kobe-u.ac.jp/pbsugar/](sugar) v1.1.1.
3. 