#Analysis of a Database Reconstruction Attack on a Public Database

In recent years, a certain type of malicious database attack,
the database reconstruction attack, has become increasingly
more feasible due to rapid advances in attack algorithm 
sophistication. Here, we will discuss how these attacks
function, demonstrate their effectiveness and efficiency,
and provide solutions for defending against such an attack.

This paper will answer the following questions:

1. What is a database reconstruction attack (DRA)?
2. To what extent are modern DRAs effective in reconstructing 
the ground truth data?
3. How scalable are DRAs with database size?
4. How can a statistical agency guard public data against a DRA without 
significantly impacting the accuracy of the data?

We will also develop a vocabulary to facilitate the discussion
of database privacy and formally define some important terms. 

Keywords: Database Reconstruction Attack, SAT solver, privacy, 
disclosure avoidance

##Problem Background

Malicious people often seek to identify individuals from publicly
available data products such as tables and graphs. 
Defending against such privacy breaches is 
a high priority for statistical agencies, and so researchers
have developed a variety of techniques to prevent database users
from identifying any Personally Identifiable Information (PII)

These techniques include:
1. **Cell Suppression**, where the values of cells with small counts or few possible
generating combinations are removed from the published table
2. **Row Swapping**, where the data rows corresponding to individuals 
with similar values in certain key cells are switched
3. **Bucketing**, where numerical values are grouped into 
buckets corresponding to ranges, instead of giving the exact
values for each entry in the table
4. **'Topcoding'**, where the buckets at the high and low ends
of the table are given without upper or lower bound (e.g. 
reporting the highest bucket for age as "80+" instead of 
"80-90" and "90-100")


The goal of a Database Reconstruction Attack is to 
use public data to create a mathematical system of equations,
which then can be used to reconstruct the original (before the disclosure
avoidance techniques were applied) data set.
While the above techniques are not without merit, this paper will
demonstrate that they alone are insufficient in guarding data against
a modern DRA. 

##Vocabulary
**Should there be a vocab section, or just in body when discussed?**

* **Database Reconstruction Attack (DRA)** - an attempt to determine survey 
response information from a publicly available data set which has had
disclosure avoidance techniques applied to it.

* **Constraint Equation** - A mathematical equation that represents 
information known to be true for a set of data.

* **Solution Universe (U)** - The set of all combinations of a 
group of variables that satisfies a certain set of constraint equations.

* **SAT Solver** - A program that uses a complex set of heuristics
to find the solution universe given a set of constraint equations.

* **Noise Addition** - The addition of small random numbers to 
statistical table values before
publication for the purpose of protecting respondent privacy.

##The Database Reconstruction Attack: An Example

To understand how a DRA works, let us 
consider a simple example data table generated from the following
survey given to two households:

**Please provide the following for each member of your family:
Age, Sex, Race, Generation.**

Here are the survey responses (the 'ground truth'):

Household #1:
* 24 Male White Parent 
* 28 Female Black Parent 
* 55 Female White Grandparent 
* 5 Female Black Child 
* 8 Male White Child

Household #2:
* 50 Male White Parent 
* 45 Male White Parent 
* 15 Female White Child 
* 17 Female White Child

The statistical agency publishes the following data based
on the survey (**Needs to be tabulated**):  

Format: Group, Number, Average Age 
 
\# Individuals: 9 27.44  
Males: 4 31.75  
Females: 5 24  
Parents: 4 36.75  
Grandparents: 1 XXX  
Children 0-12: 2 6.5  
Children 13-17: 2 16  
Whites: 7 30.57  
Blacks: 2 16.5  
Black parents: 1 XXX  
Blacks under 18: 1 XXX  
White parents: 3 39.66  
Whites under 18: 3 13.33  
Households: 2 27.875  
Avg. household size: 4.5  
Avg. # of children per household: 2 

Notice that the agency has applied cell suppression to the cells
marked XXX. This is because only one individual generated
the data in those cells, so the value is easily matched to 
that person.

Retabulating these results in a numerical format with the key  
Male = 0
Female = 1
White = 0
Black = 1
Child = 0
Parent = 1
Grandparent = 2
gives:  
(**Needs to be tabulated**) 
 
ID HOUSEHOLD AGE SEX RACE GENDER  
1 1 24 0 0 1  
2 1 28 1 1 1  
3 1 55 1 0 2  
4 1 5 1 1 0  
5 1 8 0 0 0  
6 2 50 0 0 1  
7 2 45 1 0 0  
8 2 15 1 0 0  
9 2 17 1 0 0 

The above table is the database that the attacker wishes to 
reconstruct. At the start of the attack, the attacker writes 
the following table of 45 unknowns. (**Needs to be tabulated**):

ID HH AGE SEX RACE GEN  
1 H1 A1 S1 R1 G1  
2 H2 A2 S2 R2 G2  
3 H3 A3 S3 R3 G3  
4 H4 A4 S4 R4 G4  
5 H5 A5 S5 R5 G5  
6 H6 A6 S6 R6 G6  
7 H7 A7 S7 R7 G7  
8 H8 A8 S8 R8 G8  
9 H9 A9 S9 R9 G9 

The reconstruction attack works by identifying constraint
equations given by the data table. For example, we have the
following statistic: 
 
**Individuals: 9, 27.44**  

This can be written as a linear constraint equation:  
INTEGER(((A1 + A2 + A3 + A4 + A5 + A6 + A7 + A8 + A9) * 100 / 9 ) + 0.5) = 2744

* Note - Mathematical transformations are to avoid rounding errors.

This equation is in 9 unknowns, and so is unsolvable alone. 
However, the attacker can write more constraint equations. 

**Grandparents: 1, XXX**

Becomes:  

(G1==2) + (G2==2) + (G3==2) + (G4==2) + 
(G5==2)+ (G6==2) + (G7==2) + (G8==2) + (G9==2) = 1

* Note - X==Y evaluates to 0 if X≠Y and 1 if X=Y

**Children 0-12: 2, 6.5**

Becomes:  

(G1==0) + (G2==0) + (G3==0) + (G4==0) + 
(G5==0) + (G6==0) + (G7==0) + (G8==0) + G9==0) = 2

and:

(A1 * (G1==0) + A2 * (G2==0) + A3 * (G3==0) + A4 * (G4==0) + 
A5 * (G5==0) + A6 * (G6==0) + A7 * (G7==0) + 
A8 * (G8==0) + A9 * (G9==0)) = 13

Once the attacker has converted all the published statistics
into equations like the ones above, he will have a system
of a large number of equations in 45 unknowns. 
This system has one 'true' solution, Sg, equivalent to the 
ground truth, and possibly many other 'false' solutions, {S1...Sn}. 

The Solution Universe, **U**, is potentially originally quite large:  

**U = {S1...Sn}**

However, each time the agency publishes a new statistic, the attacker
can generate new constraints and therefore narrow
down the set of possible solutions. Eventually, the attacker
will obtain **U = {Sg}**, at which point he has 
found the ground truth and reconstructed the database
successfully. Note here that the cell suppression disclosure avoidance
technique does not prevent the attacker from performing
the reconstruction attack, but rather simply gives him one
fewer constraint to work with per cell suppressed.

Even if the number of constraints is insufficient to narrow down U
to just one element, personal data can often still be identified 
because of the high probability that all remaining possible solutions 
will share the same values for a certain person. For example, if   
**U = {S1, S2}** and S1 and S2 both have values **{h1, a1, s1, r1, g1}** in common
(represented mathematically by **S1 ∩ S2 = {H1=h1, A1=a1, S1=s1, R1=r1, G1=g1}**),  
then we know that **{h1, a1, a1, r1, g1}** must be an actual person in 
the ground truth set. Thus, the database has failed to protect user privacy
even though the attack did not fully reconstruct the database.

###Methods of Attack

The three most common and effective ways of solving a 
system of constraint equations are:
1. Brute Force - trying every possible combination of solutions.
2. Creating a single cost function from the constraints, and then solve
the cost function using optimization software. 
3. Use a SAT solver, which are complex programs that solve Boolean
algebra problems. 

For large data sets such as the U.S. Census, brute force is infeasible
due to the fact that the runtime of brute force programs
scales exponentially with the number of unknowns. However,
cost functions and SAT solvers are both quite effective because they
can reduce the runtime of the program to acceptable levels.
Recent advances in SAT solver heuristics have enabled these programs
to solve systems with *millions* of variables in linear time.
In later examples, we will use a SAT solver to demonstrate
how quickly these very complex programs can solve large systems
of equations.

##The SAT Solver: Scalability and Efficacy

To demonstrate the real capabilities of the SAT solver when faced
with a very large constraint system, in contrast to our above small
example, we will use a system with 155 variables and 1135 boolean clauses.
This system results from the CNF encoding of a famous problem
known as the [Zebra Problem](http://www.ics.uci.edu/~csp/r8.pdf).
This problem is appropriate because it closely models the current format of a 
Census data publication. The writer receives the survey answers from the respondents,
redacts much of the information to avoid giving away PII, and then
publishes a data product.  

The size of this problem more closely approximates the number
of variables an attacker would need to generate constraints for
when performing a DRA through queries on a massive public data set. It is too complex
for the vast majority of humans to solve in any reasonable time. 

This problem is stated as follows: 

   1.  Five people have five different pets, smoke five different
       brands of cigarettes, have five different favorite drinks and
       live in five different houses.
   2.  The Englishman lives in the red house.
   3.  The Spaniard has a dog.
   4.  The Ukranian drinks tea.
   5.  The Norwegian lives in the leftmost house.
   6.  The Japanese smokes Parliaments.
   7.  The Norwegian lives next to the blue house.
   8.  Coffee is drunk in the green house.
   9.  The snail owner smokes Old Gold.
   10. The inhabitant of the yellow house smokes Kools.
   11. The Lucky Strikes smoker drinks orange juice.
   12. Milk is drunk in the middle house.
   13. The green house is immediately to the right of the ivory house.
   14. The Chesterfield smoker lives next door to the fox owner.
   15. The Kools smoker lives next door to where the horse is kept.

   Given these conditions, determine who owns the zebra and who drinks
   water.  
   (The attacker is 'targeting' the water drinker and the zebra owner.)  
   
Just as demonstrated in the previous example, this problem
can be encoded as a large set of boolean equations. The problem
gives 15 explicit constraints which allow the attacker to begin to generate
more constraints, and each of the combinations of variables (five people, 
five houses, five drinks, etc.) can be represented as a boolean variable, for
example, "The Norwegian lives in the red house == False"

Once the attacker has generated every constraint possible from the
given information, he can input the constraints into a SAT solver. 
In this example, we run the zebra problem through the open-source, freely available software
PicoSAT written in C. 

The results: (**tabulate in latex**)  
~~~
Solving for all solutions...  
Solution:  [-1, -2, 3, -4, -5, -6, -7, -8, -9, 10..., -152, -153, 154, -155]  
Number of solutions found in  0.0004699230194091797 seconds:  1
~~~

PicoSAT is able to solve this very complex problem in a fraction
of a second, and has reconstructed the entire database, thus
obtaining the PII of all the residents of the village despite the 
fact that the vast majority of their information was redacted by the
problem writer before release. 

The success of this attack demonstrates the inefficacy of 
cell suppression as a method for protecting PII against
a SAT solver-driven DRA. This problem
contained far more suppressed cells than unsuppressed ones, which is 
not realistic given that a real publishing agency would want to minimize
the number of suppressed cells. Despite this over-suppression, 
the SAT solver was still able to easily solve for the values of all cells in the example.

##Defending Against a DRA

As demonstrated above, new techniques must be developed in 
order to protect databases against reconstruction attacks.
One recently developed technique that has proven effective against
the DRA is a special type of noise addition called the 
[Laplace Mechanism](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf).
The mathematics behind this process are beyond the scope of this paper,
but the important property of this distribution is that it is effective
in creating noise that makes the task of the database reconstruction
attacker much more difficult.

###How Noise Addition Defeats Attacks

Zebra problem doesn't work here because it has no integer
values, just booleans. We need to make a numerical example.
