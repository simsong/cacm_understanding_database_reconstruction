/*
                          The Zebra Problem

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
*/

/*
   Run this file through a C preprocessor to turn it into a CNF formula
   in the DIMACS suggested format.  For example:
                % cc -E zebra.c | tail +2 > zebra.cnf
   (gcc's preprocessor doesn't work, because it inserts spaces between
   minus signs and numbers, making negative numbers impossible to parse.)
*/

c The zebra problem.  From Rina Dechter, "Enhancement Schemes for
c Constraint Processing:  Backjumping, Learning, and Cutset Decomposition",
c AIJ 41:273-312.  Encoded in CNF by Jon Freeman, November 1994.  I have
c found three solutions; there may be more.
c
p cnf 155 1135

#define EOC 0    /* End of clause marker */

#define englishman_house0 1
#define englishman_house1 2
#define englishman_house2 3
#define englishman_house3 4
#define englishman_house4 5

#define japanese_house0   6
#define japanese_house1   7
#define japanese_house2   8
#define japanese_house3   9
#define japanese_house4   10

#define norwegian_house0  11
#define norwegian_house1  12
#define norwegian_house2  13
#define norwegian_house3  14
#define norwegian_house4  15

#define spaniard_house0   16
#define spaniard_house1   17
#define spaniard_house2   18
#define spaniard_house3   19
#define spaniard_house4   20

#define ukranian_house0   21
#define ukranian_house1   22
#define ukranian_house2   23
#define ukranian_house3   24
#define ukranian_house4   25

/* ======================================================================= */

#define englishman_zebra  26
#define englishman_dog    27
#define englishman_horse  28
#define englishman_fox    29
#define englishman_snails 30

#define japanese_zebra    31
#define japanese_dog      32
#define japanese_horse    33
#define japanese_fox      34
#define japanese_snails   35

#define norwegian_zebra   36
#define norwegian_dog     37
#define norwegian_horse   38
#define norwegian_fox     39
#define norwegian_snails  40

#define spaniard_zebra    41
#define spaniard_dog      42
#define spaniard_horse    43
#define spaniard_fox      44
#define spaniard_snails   45

#define ukranian_zebra    46
#define ukranian_dog      47
#define ukranian_horse    48
#define ukranian_fox      49
#define ukranian_snails   50

/* ======================================================================= */

#define englishman_redHouse    51
#define englishman_greenHouse  52
#define englishman_ivoryHouse  53
#define englishman_yellowHouse 54
#define englishman_blueHouse   55

#define japanese_redHouse      56
#define japanese_greenHouse    57
#define japanese_ivoryHouse    58
#define japanese_yellowHouse   59
#define japanese_blueHouse     60

#define norwegian_redHouse     61
#define norwegian_greenHouse   62
#define norwegian_ivoryHouse   63
#define norwegian_yellowHouse  64
#define norwegian_blueHouse    65

#define spaniard_redHouse      66
#define spaniard_greenHouse    67
#define spaniard_ivoryHouse    68
#define spaniard_yellowHouse   69
#define spaniard_blueHouse     70

#define ukranian_redHouse      71
#define ukranian_greenHouse    72
#define ukranian_ivoryHouse    73
#define ukranian_yellowHouse   74
#define ukranian_blueHouse     75

/* ======================================================================= */

#define englishman_oldGold      76
#define englishman_parliament   77
#define englishman_kools        78
#define englishman_lucky        79
#define englishman_chesterfield 80

#define japanese_oldGold        81
#define japanese_parliament     82
#define japanese_kools          83
#define japanese_lucky          84
#define japanese_chesterfield   85

#define norwegian_oldGold       86
#define norwegian_parliament    87
#define norwegian_kools         88
#define norwegian_lucky         89
#define norwegian_chesterfield  90

#define spaniard_oldGold        91
#define spaniard_parliament     92
#define spaniard_kools          93
#define spaniard_lucky          94
#define spaniard_chesterfield   95

#define ukranian_oldGold        96
#define ukranian_parliament     97
#define ukranian_kools          98
#define ukranian_lucky          99
#define ukranian_chesterfield   100

/* ======================================================================= */

#define englishman_coffee      101
#define englishman_tea         102
#define englishman_orangeJuice 103
#define englishman_water       104
#define englishman_milk        105

#define japanese_coffee        106
#define japanese_tea           107
#define japanese_orangeJuice   108
#define japanese_water         109
#define japanese_milk          110

#define norwegian_coffee       111
#define norwegian_tea          112
#define norwegian_orangeJuice  113
#define norwegian_water        114
#define norwegian_milk         115

#define spaniard_coffee        116
#define spaniard_tea           117
#define spaniard_orangeJuice   118
#define spaniard_water         119
#define spaniard_milk          120

#define ukranian_coffee        121
#define ukranian_tea           122
#define ukranian_orangeJuice   123
#define ukranian_water         124
#define ukranian_milk          125

/* ======================================================================= */

#define E_immLeft_J 126
#define E_immLeft_N 127
#define E_immLeft_S 128
#define E_immLeft_U 129

#define J_immLeft_E 130
#define J_immLeft_N 131
#define J_immLeft_S 132
#define J_immLeft_U 133

#define N_immLeft_E 134
#define N_immLeft_J 135
#define N_immLeft_S 136
#define N_immLeft_U 137

#define S_immLeft_E 138
#define S_immLeft_J 139
#define S_immLeft_N 140
#define S_immLeft_U 141

#define U_immLeft_E 142
#define U_immLeft_J 143
#define U_immLeft_N 144
#define U_immLeft_S 145

/* ======================================================================= */

#define E_nextTo_J 146
#define E_nextTo_N 147
#define E_nextTo_S 148
#define E_nextTo_U 149

#define J_nextTo_E E_nextTo_J
#define J_nextTo_N 150
#define J_nextTo_S 151
#define J_nextTo_U 152

#define N_nextTo_E E_nextTo_N
#define N_nextTo_J J_nextTo_N
#define N_nextTo_S 153
#define N_nextTo_U 154

#define S_nextTo_E E_nextTo_S
#define S_nextTo_J J_nextTo_S
#define S_nextTo_N N_nextTo_S
#define S_nextTo_U 155

#define U_nextTo_E E_nextTo_U
#define U_nextTo_J J_nextTo_U
#define U_nextTo_N N_nextTo_U
#define U_nextTo_S S_nextTo_U

/* ======================================================================= */

/* Basic constraints. */


/* The Englishman lives in exactly one house. */
englishman_house0 englishman_house1 englishman_house2
englishman_house3 englishman_house4 EOC
-englishman_house0 -englishman_house1 EOC
-englishman_house0 -englishman_house2 EOC
-englishman_house0 -englishman_house3 EOC
-englishman_house0 -englishman_house4 EOC
-englishman_house1 -englishman_house2 EOC
-englishman_house1 -englishman_house3 EOC
-englishman_house1 -englishman_house4 EOC
-englishman_house2 -englishman_house3 EOC
-englishman_house2 -englishman_house4 EOC
-englishman_house3 -englishman_house4 EOC

/* The Japanese lives in exactly one house. */
japanese_house0 japanese_house1 japanese_house2
japanese_house3 japanese_house4 EOC
-japanese_house0 -japanese_house1 EOC
-japanese_house0 -japanese_house2 EOC
-japanese_house0 -japanese_house3 EOC
-japanese_house0 -japanese_house4 EOC
-japanese_house1 -japanese_house2 EOC
-japanese_house1 -japanese_house3 EOC
-japanese_house1 -japanese_house4 EOC
-japanese_house2 -japanese_house3 EOC
-japanese_house2 -japanese_house4 EOC
-japanese_house3 -japanese_house4 EOC

/* The Norwegian lives in exactly one house. */
norwegian_house0 norwegian_house1 norwegian_house2
norwegian_house3 norwegian_house4 EOC
-norwegian_house0 -norwegian_house1 EOC
-norwegian_house0 -norwegian_house2 EOC
-norwegian_house0 -norwegian_house3 EOC
-norwegian_house0 -norwegian_house4 EOC
-norwegian_house1 -norwegian_house2 EOC
-norwegian_house1 -norwegian_house3 EOC
-norwegian_house1 -norwegian_house4 EOC
-norwegian_house2 -norwegian_house3 EOC
-norwegian_house2 -norwegian_house4 EOC
-norwegian_house3 -norwegian_house4 EOC

/* The Spaniard lives in exactly one house. */
spaniard_house0 spaniard_house1 spaniard_house2
spaniard_house3 spaniard_house4 EOC
-spaniard_house0 -spaniard_house1 EOC
-spaniard_house0 -spaniard_house2 EOC
-spaniard_house0 -spaniard_house3 EOC
-spaniard_house0 -spaniard_house4 EOC
-spaniard_house1 -spaniard_house2 EOC
-spaniard_house1 -spaniard_house3 EOC
-spaniard_house1 -spaniard_house4 EOC
-spaniard_house2 -spaniard_house3 EOC
-spaniard_house2 -spaniard_house4 EOC
-spaniard_house3 -spaniard_house4 EOC

/* The Ukranian lives in exactly one house. */
ukranian_house0 ukranian_house1 ukranian_house2
ukranian_house3 ukranian_house4 EOC
-ukranian_house0 -ukranian_house1 EOC
-ukranian_house0 -ukranian_house2 EOC
-ukranian_house0 -ukranian_house3 EOC
-ukranian_house0 -ukranian_house4 EOC
-ukranian_house1 -ukranian_house2 EOC
-ukranian_house1 -ukranian_house3 EOC
-ukranian_house1 -ukranian_house4 EOC
-ukranian_house2 -ukranian_house3 EOC
-ukranian_house2 -ukranian_house4 EOC
-ukranian_house3 -ukranian_house4 EOC


/* The Englishman's house has exactly one color. */
englishman_redHouse englishman_greenHouse englishman_ivoryHouse
englishman_yellowHouse englishman_blueHouse EOC
-englishman_redHouse -englishman_greenHouse EOC
-englishman_redHouse -englishman_ivoryHouse EOC
-englishman_redHouse -englishman_yellowHouse EOC
-englishman_redHouse -englishman_blueHouse EOC
-englishman_greenHouse -englishman_ivoryHouse EOC
-englishman_greenHouse -englishman_yellowHouse EOC
-englishman_greenHouse -englishman_blueHouse EOC
-englishman_ivoryHouse -englishman_yellowHouse EOC
-englishman_ivoryHouse -englishman_blueHouse EOC
-englishman_yellowHouse -englishman_blueHouse EOC

/* The Japanese's house has exactly one color. */
japanese_redHouse japanese_greenHouse japanese_ivoryHouse
japanese_yellowHouse japanese_blueHouse EOC
-japanese_redHouse -japanese_greenHouse EOC
-japanese_redHouse -japanese_ivoryHouse EOC
-japanese_redHouse -japanese_yellowHouse EOC
-japanese_redHouse -japanese_blueHouse EOC
-japanese_greenHouse -japanese_ivoryHouse EOC
-japanese_greenHouse -japanese_yellowHouse EOC
-japanese_greenHouse -japanese_blueHouse EOC
-japanese_ivoryHouse -japanese_yellowHouse EOC
-japanese_ivoryHouse -japanese_blueHouse EOC
-japanese_yellowHouse -japanese_blueHouse EOC

/* The Norwegian's house has exactly one color. */
norwegian_redHouse norwegian_greenHouse norwegian_ivoryHouse
norwegian_yellowHouse norwegian_blueHouse EOC
-norwegian_redHouse -norwegian_greenHouse EOC
-norwegian_redHouse -norwegian_ivoryHouse EOC
-norwegian_redHouse -norwegian_yellowHouse EOC
-norwegian_redHouse -norwegian_blueHouse EOC
-norwegian_greenHouse -norwegian_ivoryHouse EOC
-norwegian_greenHouse -norwegian_yellowHouse EOC
-norwegian_greenHouse -norwegian_blueHouse EOC
-norwegian_ivoryHouse -norwegian_yellowHouse EOC
-norwegian_ivoryHouse -norwegian_blueHouse EOC
-norwegian_yellowHouse -norwegian_blueHouse EOC

/* The Spaniard's house has exactly one color. */
spaniard_redHouse spaniard_greenHouse spaniard_ivoryHouse
spaniard_yellowHouse spaniard_blueHouse EOC
-spaniard_redHouse -spaniard_greenHouse EOC
-spaniard_redHouse -spaniard_ivoryHouse EOC
-spaniard_redHouse -spaniard_yellowHouse EOC
-spaniard_redHouse -spaniard_blueHouse EOC
-spaniard_greenHouse -spaniard_ivoryHouse EOC
-spaniard_greenHouse -spaniard_yellowHouse EOC
-spaniard_greenHouse -spaniard_blueHouse EOC
-spaniard_ivoryHouse -spaniard_yellowHouse EOC
-spaniard_ivoryHouse -spaniard_blueHouse EOC
-spaniard_yellowHouse -spaniard_blueHouse EOC

/* The Ukranian's house has exactly one color. */
ukranian_redHouse ukranian_greenHouse ukranian_ivoryHouse
ukranian_yellowHouse ukranian_blueHouse EOC
-ukranian_redHouse -ukranian_greenHouse EOC
-ukranian_redHouse -ukranian_ivoryHouse EOC
-ukranian_redHouse -ukranian_yellowHouse EOC
-ukranian_redHouse -ukranian_blueHouse EOC
-ukranian_greenHouse -ukranian_ivoryHouse EOC
-ukranian_greenHouse -ukranian_yellowHouse EOC
-ukranian_greenHouse -ukranian_blueHouse EOC
-ukranian_ivoryHouse -ukranian_yellowHouse EOC
-ukranian_ivoryHouse -ukranian_blueHouse EOC
-ukranian_yellowHouse -ukranian_blueHouse EOC


/* The Englishman owns exactly one pet. */
englishman_zebra englishman_dog englishman_horse
englishman_fox englishman_snails EOC
-englishman_zebra -englishman_dog EOC
-englishman_zebra -englishman_horse EOC
-englishman_zebra -englishman_fox EOC
-englishman_zebra -englishman_snails EOC
-englishman_dog -englishman_horse EOC
-englishman_dog -englishman_fox EOC
-englishman_dog -englishman_snails EOC
-englishman_horse -englishman_fox EOC
-englishman_horse -englishman_snails EOC
-englishman_fox -englishman_snails EOC

/* The Japanese owns exactly one pet. */
japanese_zebra japanese_dog japanese_horse
japanese_fox japanese_snails EOC
-japanese_zebra -japanese_dog EOC
-japanese_zebra -japanese_horse EOC
-japanese_zebra -japanese_fox EOC
-japanese_zebra -japanese_snails EOC
-japanese_dog -japanese_horse EOC
-japanese_dog -japanese_fox EOC
-japanese_dog -japanese_snails EOC
-japanese_horse -japanese_fox EOC
-japanese_horse -japanese_snails EOC
-japanese_fox -japanese_snails EOC

/* The Norwegian owns exactly one pet. */
norwegian_zebra norwegian_dog norwegian_horse
norwegian_fox norwegian_snails EOC
-norwegian_zebra -norwegian_dog EOC
-norwegian_zebra -norwegian_horse EOC
-norwegian_zebra -norwegian_fox EOC
-norwegian_zebra -norwegian_snails EOC
-norwegian_dog -norwegian_horse EOC
-norwegian_dog -norwegian_fox EOC
-norwegian_dog -norwegian_snails EOC
-norwegian_horse -norwegian_fox EOC
-norwegian_horse -norwegian_snails EOC
-norwegian_fox -norwegian_snails EOC

/* The Spaniard owns exactly one pet. */
spaniard_zebra spaniard_dog spaniard_horse
spaniard_fox spaniard_snails EOC
-spaniard_zebra -spaniard_dog EOC
-spaniard_zebra -spaniard_horse EOC
-spaniard_zebra -spaniard_fox EOC
-spaniard_zebra -spaniard_snails EOC
-spaniard_dog -spaniard_horse EOC
-spaniard_dog -spaniard_fox EOC
-spaniard_dog -spaniard_snails EOC
-spaniard_horse -spaniard_fox EOC
-spaniard_horse -spaniard_snails EOC
-spaniard_fox -spaniard_snails EOC

/* The Ukranian owns exactly one pet. */
ukranian_zebra ukranian_dog ukranian_horse
ukranian_fox ukranian_snails EOC
-ukranian_zebra -ukranian_dog EOC
-ukranian_zebra -ukranian_horse EOC
-ukranian_zebra -ukranian_fox EOC
-ukranian_zebra -ukranian_snails EOC
-ukranian_dog -ukranian_horse EOC
-ukranian_dog -ukranian_fox EOC
-ukranian_dog -ukranian_snails EOC
-ukranian_horse -ukranian_fox EOC
-ukranian_horse -ukranian_snails EOC
-ukranian_fox -ukranian_snails EOC


/* The Englishman has exactly one favorite drink. */
englishman_coffee englishman_tea englishman_orangeJuice
englishman_water englishman_milk EOC
-englishman_coffee -englishman_tea EOC
-englishman_coffee -englishman_orangeJuice EOC
-englishman_coffee -englishman_water EOC
-englishman_coffee -englishman_milk EOC
-englishman_tea -englishman_orangeJuice EOC
-englishman_tea -englishman_water EOC
-englishman_tea -englishman_milk EOC
-englishman_orangeJuice -englishman_water EOC
-englishman_orangeJuice -englishman_milk EOC
-englishman_water -englishman_milk EOC

/* The Japanese has exactly one favorite drink. */
japanese_coffee japanese_tea japanese_orangeJuice
japanese_water japanese_milk EOC
-japanese_coffee -japanese_tea EOC
-japanese_coffee -japanese_orangeJuice EOC
-japanese_coffee -japanese_water EOC
-japanese_coffee -japanese_milk EOC
-japanese_tea -japanese_orangeJuice EOC
-japanese_tea -japanese_water EOC
-japanese_tea -japanese_milk EOC
-japanese_orangeJuice -japanese_water EOC
-japanese_orangeJuice -japanese_milk EOC
-japanese_water -japanese_milk EOC

/* The Norwegian has exactly one favorite drink. */
norwegian_coffee norwegian_tea norwegian_orangeJuice
norwegian_water norwegian_milk EOC
-norwegian_coffee -norwegian_tea EOC
-norwegian_coffee -norwegian_orangeJuice EOC
-norwegian_coffee -norwegian_water EOC
-norwegian_coffee -norwegian_milk EOC
-norwegian_tea -norwegian_orangeJuice EOC
-norwegian_tea -norwegian_water EOC
-norwegian_tea -norwegian_milk EOC
-norwegian_orangeJuice -norwegian_water EOC
-norwegian_orangeJuice -norwegian_milk EOC
-norwegian_water -norwegian_milk EOC

/* The Spaniard has exactly one favorite drink. */
spaniard_coffee spaniard_tea spaniard_orangeJuice
spaniard_water spaniard_milk EOC
-spaniard_coffee -spaniard_tea EOC
-spaniard_coffee -spaniard_orangeJuice EOC
-spaniard_coffee -spaniard_water EOC
-spaniard_coffee -spaniard_milk EOC
-spaniard_tea -spaniard_orangeJuice EOC
-spaniard_tea -spaniard_water EOC
-spaniard_tea -spaniard_milk EOC
-spaniard_orangeJuice -spaniard_water EOC
-spaniard_orangeJuice -spaniard_milk EOC
-spaniard_water -spaniard_milk EOC

/* The Ukranian has exactly one favorite drink. */
ukranian_coffee ukranian_tea ukranian_orangeJuice
ukranian_water ukranian_milk EOC
-ukranian_coffee -ukranian_tea EOC
-ukranian_coffee -ukranian_orangeJuice EOC
-ukranian_coffee -ukranian_water EOC
-ukranian_coffee -ukranian_milk EOC
-ukranian_tea -ukranian_orangeJuice EOC
-ukranian_tea -ukranian_water EOC
-ukranian_tea -ukranian_milk EOC
-ukranian_orangeJuice -ukranian_water EOC
-ukranian_orangeJuice -ukranian_milk EOC
-ukranian_water -ukranian_milk EOC


/* The Englishman smokes exactly one brand of cigarette. */
englishman_oldGold englishman_parliament englishman_kools
englishman_lucky englishman_chesterfield EOC
-englishman_oldGold -englishman_parliament EOC
-englishman_oldGold -englishman_kools EOC
-englishman_oldGold -englishman_lucky EOC
-englishman_oldGold -englishman_chesterfield EOC
-englishman_parliament -englishman_kools EOC
-englishman_parliament -englishman_lucky EOC
-englishman_parliament -englishman_chesterfield EOC
-englishman_kools -englishman_lucky EOC
-englishman_kools -englishman_chesterfield EOC
-englishman_lucky -englishman_chesterfield EOC

/* The Japanese smokes exactly one brand of cigarette. */
japanese_oldGold japanese_parliament japanese_kools
japanese_lucky japanese_chesterfield EOC
-japanese_oldGold -japanese_parliament EOC
-japanese_oldGold -japanese_kools EOC
-japanese_oldGold -japanese_lucky EOC
-japanese_oldGold -japanese_chesterfield EOC
-japanese_parliament -japanese_kools EOC
-japanese_parliament -japanese_lucky EOC
-japanese_parliament -japanese_chesterfield EOC
-japanese_kools -japanese_lucky EOC
-japanese_kools -japanese_chesterfield EOC
-japanese_lucky -japanese_chesterfield EOC

/* The Norwegian smokes exactly one brand of cigarette. */
norwegian_oldGold norwegian_parliament norwegian_kools
norwegian_lucky norwegian_chesterfield EOC
-norwegian_oldGold -norwegian_parliament EOC
-norwegian_oldGold -norwegian_kools EOC
-norwegian_oldGold -norwegian_lucky EOC
-norwegian_oldGold -norwegian_chesterfield EOC
-norwegian_parliament -norwegian_kools EOC
-norwegian_parliament -norwegian_lucky EOC
-norwegian_parliament -norwegian_chesterfield EOC
-norwegian_kools -norwegian_lucky EOC
-norwegian_kools -norwegian_chesterfield EOC
-norwegian_lucky -norwegian_chesterfield EOC

/* The Spaniard smokes exactly one brand of cigarette. */
spaniard_oldGold spaniard_parliament spaniard_kools
spaniard_lucky spaniard_chesterfield EOC
-spaniard_oldGold -spaniard_parliament EOC
-spaniard_oldGold -spaniard_kools EOC
-spaniard_oldGold -spaniard_lucky EOC
-spaniard_oldGold -spaniard_chesterfield EOC
-spaniard_parliament -spaniard_kools EOC
-spaniard_parliament -spaniard_lucky EOC
-spaniard_parliament -spaniard_chesterfield EOC
-spaniard_kools -spaniard_lucky EOC
-spaniard_kools -spaniard_chesterfield EOC
-spaniard_lucky -spaniard_chesterfield EOC

/* The Ukranian smokes exactly one brand of cigarette. */
ukranian_oldGold ukranian_parliament ukranian_kools
ukranian_lucky ukranian_chesterfield EOC
-ukranian_oldGold -ukranian_parliament EOC
-ukranian_oldGold -ukranian_kools EOC
-ukranian_oldGold -ukranian_lucky EOC
-ukranian_oldGold -ukranian_chesterfield EOC
-ukranian_parliament -ukranian_kools EOC
-ukranian_parliament -ukranian_lucky EOC
-ukranian_parliament -ukranian_chesterfield EOC
-ukranian_kools -ukranian_lucky EOC
-ukranian_kools -ukranian_chesterfield EOC
-ukranian_lucky -ukranian_chesterfield EOC


/* Other basic constraints about physical location. */

/* Positive constraints about one house being immediately to the
   right of another. */
-englishman_house0 -japanese_house1 E_immLeft_J EOC
-englishman_house1 -japanese_house2 E_immLeft_J EOC
-englishman_house2 -japanese_house3 E_immLeft_J EOC
-englishman_house3 -japanese_house4 E_immLeft_J EOC

-englishman_house0 -norwegian_house1 E_immLeft_N EOC
-englishman_house1 -norwegian_house2 E_immLeft_N EOC
-englishman_house2 -norwegian_house3 E_immLeft_N EOC
-englishman_house3 -norwegian_house4 E_immLeft_N EOC

-englishman_house0 -spaniard_house1 E_immLeft_S EOC
-englishman_house1 -spaniard_house2 E_immLeft_S EOC
-englishman_house2 -spaniard_house3 E_immLeft_S EOC
-englishman_house3 -spaniard_house4 E_immLeft_S EOC

-englishman_house0 -ukranian_house1 E_immLeft_U EOC
-englishman_house1 -ukranian_house2 E_immLeft_U EOC
-englishman_house2 -ukranian_house3 E_immLeft_U EOC
-englishman_house3 -ukranian_house4 E_immLeft_U EOC

-japanese_house0 -englishman_house1 J_immLeft_E EOC
-japanese_house1 -englishman_house2 J_immLeft_E EOC
-japanese_house2 -englishman_house3 J_immLeft_E EOC
-japanese_house3 -englishman_house4 J_immLeft_E EOC

-japanese_house0 -norwegian_house1 J_immLeft_N EOC
-japanese_house1 -norwegian_house2 J_immLeft_N EOC
-japanese_house2 -norwegian_house3 J_immLeft_N EOC
-japanese_house3 -norwegian_house4 J_immLeft_N EOC

-japanese_house0 -spaniard_house1 J_immLeft_S EOC
-japanese_house1 -spaniard_house2 J_immLeft_S EOC
-japanese_house2 -spaniard_house3 J_immLeft_S EOC
-japanese_house3 -spaniard_house4 J_immLeft_S EOC

-japanese_house0 -ukranian_house1 J_immLeft_U EOC
-japanese_house1 -ukranian_house2 J_immLeft_U EOC
-japanese_house2 -ukranian_house3 J_immLeft_U EOC
-japanese_house3 -ukranian_house4 J_immLeft_U EOC

-norwegian_house0 -englishman_house1 N_immLeft_E EOC
-norwegian_house1 -englishman_house2 N_immLeft_E EOC
-norwegian_house2 -englishman_house3 N_immLeft_E EOC
-norwegian_house3 -englishman_house4 N_immLeft_E EOC

-norwegian_house0 -japanese_house1 N_immLeft_J EOC
-norwegian_house1 -japanese_house2 N_immLeft_J EOC
-norwegian_house2 -japanese_house3 N_immLeft_J EOC
-norwegian_house3 -japanese_house4 N_immLeft_J EOC

-norwegian_house0 -spaniard_house1 N_immLeft_S EOC
-norwegian_house1 -spaniard_house2 N_immLeft_S EOC
-norwegian_house2 -spaniard_house3 N_immLeft_S EOC
-norwegian_house3 -spaniard_house4 N_immLeft_S EOC

-norwegian_house0 -ukranian_house1 N_immLeft_U EOC
-norwegian_house1 -ukranian_house2 N_immLeft_U EOC
-norwegian_house2 -ukranian_house3 N_immLeft_U EOC
-norwegian_house3 -ukranian_house4 N_immLeft_U EOC

-spaniard_house0 -englishman_house1 S_immLeft_E EOC
-spaniard_house1 -englishman_house2 S_immLeft_E EOC
-spaniard_house2 -englishman_house3 S_immLeft_E EOC
-spaniard_house3 -englishman_house4 S_immLeft_E EOC

-spaniard_house0 -japanese_house1 S_immLeft_J EOC
-spaniard_house1 -japanese_house2 S_immLeft_J EOC
-spaniard_house2 -japanese_house3 S_immLeft_J EOC
-spaniard_house3 -japanese_house4 S_immLeft_J EOC

-spaniard_house0 -norwegian_house1 S_immLeft_N EOC
-spaniard_house1 -norwegian_house2 S_immLeft_N EOC
-spaniard_house2 -norwegian_house3 S_immLeft_N EOC
-spaniard_house3 -norwegian_house4 S_immLeft_N EOC

-spaniard_house0 -ukranian_house1 S_immLeft_U EOC
-spaniard_house1 -ukranian_house2 S_immLeft_U EOC
-spaniard_house2 -ukranian_house3 S_immLeft_U EOC
-spaniard_house3 -ukranian_house4 S_immLeft_U EOC

-ukranian_house0 -englishman_house1 U_immLeft_E EOC
-ukranian_house1 -englishman_house2 U_immLeft_E EOC
-ukranian_house2 -englishman_house3 U_immLeft_E EOC
-ukranian_house3 -englishman_house4 U_immLeft_E EOC

-ukranian_house0 -japanese_house1 U_immLeft_J EOC
-ukranian_house1 -japanese_house2 U_immLeft_J EOC
-ukranian_house2 -japanese_house3 U_immLeft_J EOC
-ukranian_house3 -japanese_house4 U_immLeft_J EOC

-ukranian_house0 -norwegian_house1 U_immLeft_N EOC
-ukranian_house1 -norwegian_house2 U_immLeft_N EOC
-ukranian_house2 -norwegian_house3 U_immLeft_N EOC
-ukranian_house3 -norwegian_house4 U_immLeft_N EOC

-ukranian_house0 -spaniard_house1 U_immLeft_S EOC
-ukranian_house1 -spaniard_house2 U_immLeft_S EOC
-ukranian_house2 -spaniard_house3 U_immLeft_S EOC
-ukranian_house3 -spaniard_house4 U_immLeft_S EOC

/* Negative constraints about one house being immediately to the
   right of another. */
-englishman_house0 -japanese_house2 -E_immLeft_J EOC
-englishman_house0 -japanese_house3 -E_immLeft_J EOC
-englishman_house0 -japanese_house4 -E_immLeft_J EOC
-englishman_house1 -japanese_house0 -E_immLeft_J EOC
-englishman_house1 -japanese_house3 -E_immLeft_J EOC
-englishman_house1 -japanese_house4 -E_immLeft_J EOC
-englishman_house2 -japanese_house0 -E_immLeft_J EOC
-englishman_house2 -japanese_house1 -E_immLeft_J EOC
-englishman_house2 -japanese_house4 -E_immLeft_J EOC
-englishman_house3 -japanese_house0 -E_immLeft_J EOC
-englishman_house3 -japanese_house1 -E_immLeft_J EOC
-englishman_house3 -japanese_house2 -E_immLeft_J EOC
-englishman_house4 -japanese_house0 -E_immLeft_J EOC
-englishman_house4 -japanese_house1 -E_immLeft_J EOC
-englishman_house4 -japanese_house2 -E_immLeft_J EOC
-englishman_house4 -japanese_house3 -E_immLeft_J EOC

-englishman_house0 -norwegian_house2 -E_immLeft_N EOC
-englishman_house0 -norwegian_house3 -E_immLeft_N EOC
-englishman_house0 -norwegian_house4 -E_immLeft_N EOC
-englishman_house1 -norwegian_house0 -E_immLeft_N EOC
-englishman_house1 -norwegian_house3 -E_immLeft_N EOC
-englishman_house1 -norwegian_house4 -E_immLeft_N EOC
-englishman_house2 -norwegian_house0 -E_immLeft_N EOC
-englishman_house2 -norwegian_house1 -E_immLeft_N EOC
-englishman_house2 -norwegian_house4 -E_immLeft_N EOC
-englishman_house3 -norwegian_house0 -E_immLeft_N EOC
-englishman_house3 -norwegian_house1 -E_immLeft_N EOC
-englishman_house3 -norwegian_house2 -E_immLeft_N EOC
-englishman_house4 -norwegian_house0 -E_immLeft_N EOC
-englishman_house4 -norwegian_house1 -E_immLeft_N EOC
-englishman_house4 -norwegian_house2 -E_immLeft_N EOC
-englishman_house4 -norwegian_house3 -E_immLeft_N EOC

-englishman_house0 -spaniard_house2 -E_immLeft_S EOC
-englishman_house0 -spaniard_house3 -E_immLeft_S EOC
-englishman_house0 -spaniard_house4 -E_immLeft_S EOC
-englishman_house1 -spaniard_house0 -E_immLeft_S EOC
-englishman_house1 -spaniard_house3 -E_immLeft_S EOC
-englishman_house1 -spaniard_house4 -E_immLeft_S EOC
-englishman_house2 -spaniard_house0 -E_immLeft_S EOC
-englishman_house2 -spaniard_house1 -E_immLeft_S EOC
-englishman_house2 -spaniard_house4 -E_immLeft_S EOC
-englishman_house3 -spaniard_house0 -E_immLeft_S EOC
-englishman_house3 -spaniard_house1 -E_immLeft_S EOC
-englishman_house3 -spaniard_house2 -E_immLeft_S EOC
-englishman_house4 -spaniard_house0 -E_immLeft_S EOC
-englishman_house4 -spaniard_house1 -E_immLeft_S EOC
-englishman_house4 -spaniard_house2 -E_immLeft_S EOC
-englishman_house4 -spaniard_house3 -E_immLeft_S EOC

-englishman_house0 -ukranian_house2 -E_immLeft_U EOC
-englishman_house0 -ukranian_house3 -E_immLeft_U EOC
-englishman_house0 -ukranian_house4 -E_immLeft_U EOC
-englishman_house1 -ukranian_house0 -E_immLeft_U EOC
-englishman_house1 -ukranian_house3 -E_immLeft_U EOC
-englishman_house1 -ukranian_house4 -E_immLeft_U EOC
-englishman_house2 -ukranian_house0 -E_immLeft_U EOC
-englishman_house2 -ukranian_house1 -E_immLeft_U EOC
-englishman_house2 -ukranian_house4 -E_immLeft_U EOC
-englishman_house3 -ukranian_house0 -E_immLeft_U EOC
-englishman_house3 -ukranian_house1 -E_immLeft_U EOC
-englishman_house3 -ukranian_house2 -E_immLeft_U EOC
-englishman_house4 -ukranian_house0 -E_immLeft_U EOC
-englishman_house4 -ukranian_house1 -E_immLeft_U EOC
-englishman_house4 -ukranian_house2 -E_immLeft_U EOC
-englishman_house4 -ukranian_house3 -E_immLeft_U EOC

-japanese_house0 -englishman_house2 -J_immLeft_E EOC
-japanese_house0 -englishman_house3 -J_immLeft_E EOC
-japanese_house0 -englishman_house4 -J_immLeft_E EOC
-japanese_house1 -englishman_house0 -J_immLeft_E EOC
-japanese_house1 -englishman_house3 -J_immLeft_E EOC
-japanese_house1 -englishman_house4 -J_immLeft_E EOC
-japanese_house2 -englishman_house0 -J_immLeft_E EOC
-japanese_house2 -englishman_house1 -J_immLeft_E EOC
-japanese_house2 -englishman_house4 -J_immLeft_E EOC
-japanese_house3 -englishman_house0 -J_immLeft_E EOC
-japanese_house3 -englishman_house1 -J_immLeft_E EOC
-japanese_house3 -englishman_house2 -J_immLeft_E EOC
-japanese_house4 -englishman_house0 -J_immLeft_E EOC
-japanese_house4 -englishman_house1 -J_immLeft_E EOC
-japanese_house4 -englishman_house2 -J_immLeft_E EOC
-japanese_house4 -englishman_house3 -J_immLeft_E EOC

-japanese_house0 -norwegian_house2 -J_immLeft_N EOC
-japanese_house0 -norwegian_house3 -J_immLeft_N EOC
-japanese_house0 -norwegian_house4 -J_immLeft_N EOC
-japanese_house1 -norwegian_house0 -J_immLeft_N EOC
-japanese_house1 -norwegian_house3 -J_immLeft_N EOC
-japanese_house1 -norwegian_house4 -J_immLeft_N EOC
-japanese_house2 -norwegian_house0 -J_immLeft_N EOC
-japanese_house2 -norwegian_house1 -J_immLeft_N EOC
-japanese_house2 -norwegian_house4 -J_immLeft_N EOC
-japanese_house3 -norwegian_house0 -J_immLeft_N EOC
-japanese_house3 -norwegian_house1 -J_immLeft_N EOC
-japanese_house3 -norwegian_house2 -J_immLeft_N EOC
-japanese_house4 -norwegian_house0 -J_immLeft_N EOC
-japanese_house4 -norwegian_house1 -J_immLeft_N EOC
-japanese_house4 -norwegian_house2 -J_immLeft_N EOC
-japanese_house4 -norwegian_house3 -J_immLeft_N EOC

-japanese_house0 -spaniard_house2 -J_immLeft_S EOC
-japanese_house0 -spaniard_house3 -J_immLeft_S EOC
-japanese_house0 -spaniard_house4 -J_immLeft_S EOC
-japanese_house1 -spaniard_house0 -J_immLeft_S EOC
-japanese_house1 -spaniard_house3 -J_immLeft_S EOC
-japanese_house1 -spaniard_house4 -J_immLeft_S EOC
-japanese_house2 -spaniard_house0 -J_immLeft_S EOC
-japanese_house2 -spaniard_house1 -J_immLeft_S EOC
-japanese_house2 -spaniard_house4 -J_immLeft_S EOC
-japanese_house3 -spaniard_house0 -J_immLeft_S EOC
-japanese_house3 -spaniard_house1 -J_immLeft_S EOC
-japanese_house3 -spaniard_house2 -J_immLeft_S EOC
-japanese_house4 -spaniard_house0 -J_immLeft_S EOC
-japanese_house4 -spaniard_house1 -J_immLeft_S EOC
-japanese_house4 -spaniard_house2 -J_immLeft_S EOC
-japanese_house4 -spaniard_house3 -J_immLeft_S EOC

-japanese_house0 -ukranian_house2 -J_immLeft_U EOC
-japanese_house0 -ukranian_house3 -J_immLeft_U EOC
-japanese_house0 -ukranian_house4 -J_immLeft_U EOC
-japanese_house1 -ukranian_house0 -J_immLeft_U EOC
-japanese_house1 -ukranian_house3 -J_immLeft_U EOC
-japanese_house1 -ukranian_house4 -J_immLeft_U EOC
-japanese_house2 -ukranian_house0 -J_immLeft_U EOC
-japanese_house2 -ukranian_house1 -J_immLeft_U EOC
-japanese_house2 -ukranian_house4 -J_immLeft_U EOC
-japanese_house3 -ukranian_house0 -J_immLeft_U EOC
-japanese_house3 -ukranian_house1 -J_immLeft_U EOC
-japanese_house3 -ukranian_house2 -J_immLeft_U EOC
-japanese_house4 -ukranian_house0 -J_immLeft_U EOC
-japanese_house4 -ukranian_house1 -J_immLeft_U EOC
-japanese_house4 -ukranian_house2 -J_immLeft_U EOC
-japanese_house4 -ukranian_house3 -J_immLeft_U EOC

-norwegian_house0 -englishman_house2 -N_immLeft_E EOC
-norwegian_house0 -englishman_house3 -N_immLeft_E EOC
-norwegian_house0 -englishman_house4 -N_immLeft_E EOC
-norwegian_house1 -englishman_house0 -N_immLeft_E EOC
-norwegian_house1 -englishman_house3 -N_immLeft_E EOC
-norwegian_house1 -englishman_house4 -N_immLeft_E EOC
-norwegian_house2 -englishman_house0 -N_immLeft_E EOC
-norwegian_house2 -englishman_house1 -N_immLeft_E EOC
-norwegian_house2 -englishman_house4 -N_immLeft_E EOC
-norwegian_house3 -englishman_house0 -N_immLeft_E EOC
-norwegian_house3 -englishman_house1 -N_immLeft_E EOC
-norwegian_house3 -englishman_house2 -N_immLeft_E EOC
-norwegian_house4 -englishman_house0 -N_immLeft_E EOC
-norwegian_house4 -englishman_house1 -N_immLeft_E EOC
-norwegian_house4 -englishman_house2 -N_immLeft_E EOC
-norwegian_house4 -englishman_house3 -N_immLeft_E EOC

-norwegian_house0 -japanese_house2 -N_immLeft_J EOC
-norwegian_house0 -japanese_house3 -N_immLeft_J EOC
-norwegian_house0 -japanese_house4 -N_immLeft_J EOC
-norwegian_house1 -japanese_house0 -N_immLeft_J EOC
-norwegian_house1 -japanese_house3 -N_immLeft_J EOC
-norwegian_house1 -japanese_house4 -N_immLeft_J EOC
-norwegian_house2 -japanese_house0 -N_immLeft_J EOC
-norwegian_house2 -japanese_house1 -N_immLeft_J EOC
-norwegian_house2 -japanese_house4 -N_immLeft_J EOC
-norwegian_house3 -japanese_house0 -N_immLeft_J EOC
-norwegian_house3 -japanese_house1 -N_immLeft_J EOC
-norwegian_house3 -japanese_house2 -N_immLeft_J EOC
-norwegian_house4 -japanese_house0 -N_immLeft_J EOC
-norwegian_house4 -japanese_house1 -N_immLeft_J EOC
-norwegian_house4 -japanese_house2 -N_immLeft_J EOC
-norwegian_house4 -japanese_house3 -N_immLeft_J EOC

-norwegian_house0 -spaniard_house2 -N_immLeft_S EOC
-norwegian_house0 -spaniard_house3 -N_immLeft_S EOC
-norwegian_house0 -spaniard_house4 -N_immLeft_S EOC
-norwegian_house1 -spaniard_house0 -N_immLeft_S EOC
-norwegian_house1 -spaniard_house3 -N_immLeft_S EOC
-norwegian_house1 -spaniard_house4 -N_immLeft_S EOC
-norwegian_house2 -spaniard_house0 -N_immLeft_S EOC
-norwegian_house2 -spaniard_house1 -N_immLeft_S EOC
-norwegian_house2 -spaniard_house4 -N_immLeft_S EOC
-norwegian_house3 -spaniard_house0 -N_immLeft_S EOC
-norwegian_house3 -spaniard_house1 -N_immLeft_S EOC
-norwegian_house3 -spaniard_house2 -N_immLeft_S EOC
-norwegian_house4 -spaniard_house0 -N_immLeft_S EOC
-norwegian_house4 -spaniard_house1 -N_immLeft_S EOC
-norwegian_house4 -spaniard_house2 -N_immLeft_S EOC
-norwegian_house4 -spaniard_house3 -N_immLeft_S EOC

-norwegian_house0 -ukranian_house2 -N_immLeft_U EOC
-norwegian_house0 -ukranian_house3 -N_immLeft_U EOC
-norwegian_house0 -ukranian_house4 -N_immLeft_U EOC
-norwegian_house1 -ukranian_house0 -N_immLeft_U EOC
-norwegian_house1 -ukranian_house3 -N_immLeft_U EOC
-norwegian_house1 -ukranian_house4 -N_immLeft_U EOC
-norwegian_house2 -ukranian_house0 -N_immLeft_U EOC
-norwegian_house2 -ukranian_house1 -N_immLeft_U EOC
-norwegian_house2 -ukranian_house4 -N_immLeft_U EOC
-norwegian_house3 -ukranian_house0 -N_immLeft_U EOC
-norwegian_house3 -ukranian_house1 -N_immLeft_U EOC
-norwegian_house3 -ukranian_house2 -N_immLeft_U EOC
-norwegian_house4 -ukranian_house0 -N_immLeft_U EOC
-norwegian_house4 -ukranian_house1 -N_immLeft_U EOC
-norwegian_house4 -ukranian_house2 -N_immLeft_U EOC
-norwegian_house4 -ukranian_house3 -N_immLeft_U EOC

-spaniard_house0 -englishman_house2 -S_immLeft_E EOC
-spaniard_house0 -englishman_house3 -S_immLeft_E EOC
-spaniard_house0 -englishman_house4 -S_immLeft_E EOC
-spaniard_house1 -englishman_house0 -S_immLeft_E EOC
-spaniard_house1 -englishman_house3 -S_immLeft_E EOC
-spaniard_house1 -englishman_house4 -S_immLeft_E EOC
-spaniard_house2 -englishman_house0 -S_immLeft_E EOC
-spaniard_house2 -englishman_house1 -S_immLeft_E EOC
-spaniard_house2 -englishman_house4 -S_immLeft_E EOC
-spaniard_house3 -englishman_house0 -S_immLeft_E EOC
-spaniard_house3 -englishman_house1 -S_immLeft_E EOC
-spaniard_house3 -englishman_house2 -S_immLeft_E EOC
-spaniard_house4 -englishman_house0 -S_immLeft_E EOC
-spaniard_house4 -englishman_house1 -S_immLeft_E EOC
-spaniard_house4 -englishman_house2 -S_immLeft_E EOC
-spaniard_house4 -englishman_house3 -S_immLeft_E EOC

-spaniard_house0 -japanese_house2 -S_immLeft_J EOC
-spaniard_house0 -japanese_house3 -S_immLeft_J EOC
-spaniard_house0 -japanese_house4 -S_immLeft_J EOC
-spaniard_house1 -japanese_house0 -S_immLeft_J EOC
-spaniard_house1 -japanese_house3 -S_immLeft_J EOC
-spaniard_house1 -japanese_house4 -S_immLeft_J EOC
-spaniard_house2 -japanese_house0 -S_immLeft_J EOC
-spaniard_house2 -japanese_house1 -S_immLeft_J EOC
-spaniard_house2 -japanese_house4 -S_immLeft_J EOC
-spaniard_house3 -japanese_house0 -S_immLeft_J EOC
-spaniard_house3 -japanese_house1 -S_immLeft_J EOC
-spaniard_house3 -japanese_house2 -S_immLeft_J EOC
-spaniard_house4 -japanese_house0 -S_immLeft_J EOC
-spaniard_house4 -japanese_house1 -S_immLeft_J EOC
-spaniard_house4 -japanese_house2 -S_immLeft_J EOC
-spaniard_house4 -japanese_house3 -S_immLeft_J EOC

-spaniard_house0 -norwegian_house2 -S_immLeft_N EOC
-spaniard_house0 -norwegian_house3 -S_immLeft_N EOC
-spaniard_house0 -norwegian_house4 -S_immLeft_N EOC
-spaniard_house1 -norwegian_house0 -S_immLeft_N EOC
-spaniard_house1 -norwegian_house3 -S_immLeft_N EOC
-spaniard_house1 -norwegian_house4 -S_immLeft_N EOC
-spaniard_house2 -norwegian_house0 -S_immLeft_N EOC
-spaniard_house2 -norwegian_house1 -S_immLeft_N EOC
-spaniard_house2 -norwegian_house4 -S_immLeft_N EOC
-spaniard_house3 -norwegian_house0 -S_immLeft_N EOC
-spaniard_house3 -norwegian_house1 -S_immLeft_N EOC
-spaniard_house3 -norwegian_house2 -S_immLeft_N EOC
-spaniard_house4 -norwegian_house0 -S_immLeft_N EOC
-spaniard_house4 -norwegian_house1 -S_immLeft_N EOC
-spaniard_house4 -norwegian_house2 -S_immLeft_N EOC
-spaniard_house4 -norwegian_house3 -S_immLeft_N EOC

-spaniard_house0 -ukranian_house2 -S_immLeft_U EOC
-spaniard_house0 -ukranian_house3 -S_immLeft_U EOC
-spaniard_house0 -ukranian_house4 -S_immLeft_U EOC
-spaniard_house1 -ukranian_house0 -S_immLeft_U EOC
-spaniard_house1 -ukranian_house3 -S_immLeft_U EOC
-spaniard_house1 -ukranian_house4 -S_immLeft_U EOC
-spaniard_house2 -ukranian_house0 -S_immLeft_U EOC
-spaniard_house2 -ukranian_house1 -S_immLeft_U EOC
-spaniard_house2 -ukranian_house4 -S_immLeft_U EOC
-spaniard_house3 -ukranian_house0 -S_immLeft_U EOC
-spaniard_house3 -ukranian_house1 -S_immLeft_U EOC
-spaniard_house3 -ukranian_house2 -S_immLeft_U EOC
-spaniard_house4 -ukranian_house0 -S_immLeft_U EOC
-spaniard_house4 -ukranian_house1 -S_immLeft_U EOC
-spaniard_house4 -ukranian_house2 -S_immLeft_U EOC
-spaniard_house4 -ukranian_house3 -S_immLeft_U EOC

-ukranian_house0 -englishman_house2 -U_immLeft_E EOC
-ukranian_house0 -englishman_house3 -U_immLeft_E EOC
-ukranian_house0 -englishman_house4 -U_immLeft_E EOC
-ukranian_house1 -englishman_house0 -U_immLeft_E EOC
-ukranian_house1 -englishman_house3 -U_immLeft_E EOC
-ukranian_house1 -englishman_house4 -U_immLeft_E EOC
-ukranian_house2 -englishman_house0 -U_immLeft_E EOC
-ukranian_house2 -englishman_house1 -U_immLeft_E EOC
-ukranian_house2 -englishman_house4 -U_immLeft_E EOC
-ukranian_house3 -englishman_house0 -U_immLeft_E EOC
-ukranian_house3 -englishman_house1 -U_immLeft_E EOC
-ukranian_house3 -englishman_house2 -U_immLeft_E EOC
-ukranian_house4 -englishman_house0 -U_immLeft_E EOC
-ukranian_house4 -englishman_house1 -U_immLeft_E EOC
-ukranian_house4 -englishman_house2 -U_immLeft_E EOC
-ukranian_house4 -englishman_house3 -U_immLeft_E EOC

-ukranian_house0 -japanese_house2 -U_immLeft_J EOC
-ukranian_house0 -japanese_house3 -U_immLeft_J EOC
-ukranian_house0 -japanese_house4 -U_immLeft_J EOC
-ukranian_house1 -japanese_house0 -U_immLeft_J EOC
-ukranian_house1 -japanese_house3 -U_immLeft_J EOC
-ukranian_house1 -japanese_house4 -U_immLeft_J EOC
-ukranian_house2 -japanese_house0 -U_immLeft_J EOC
-ukranian_house2 -japanese_house1 -U_immLeft_J EOC
-ukranian_house2 -japanese_house4 -U_immLeft_J EOC
-ukranian_house3 -japanese_house0 -U_immLeft_J EOC
-ukranian_house3 -japanese_house1 -U_immLeft_J EOC
-ukranian_house3 -japanese_house2 -U_immLeft_J EOC
-ukranian_house4 -japanese_house0 -U_immLeft_J EOC
-ukranian_house4 -japanese_house1 -U_immLeft_J EOC
-ukranian_house4 -japanese_house2 -U_immLeft_J EOC
-ukranian_house4 -japanese_house3 -U_immLeft_J EOC

-ukranian_house0 -norwegian_house2 -U_immLeft_N EOC
-ukranian_house0 -norwegian_house3 -U_immLeft_N EOC
-ukranian_house0 -norwegian_house4 -U_immLeft_N EOC
-ukranian_house1 -norwegian_house0 -U_immLeft_N EOC
-ukranian_house1 -norwegian_house3 -U_immLeft_N EOC
-ukranian_house1 -norwegian_house4 -U_immLeft_N EOC
-ukranian_house2 -norwegian_house0 -U_immLeft_N EOC
-ukranian_house2 -norwegian_house1 -U_immLeft_N EOC
-ukranian_house2 -norwegian_house4 -U_immLeft_N EOC
-ukranian_house3 -norwegian_house0 -U_immLeft_N EOC
-ukranian_house3 -norwegian_house1 -U_immLeft_N EOC
-ukranian_house3 -norwegian_house2 -U_immLeft_N EOC
-ukranian_house4 -norwegian_house0 -U_immLeft_N EOC
-ukranian_house4 -norwegian_house1 -U_immLeft_N EOC
-ukranian_house4 -norwegian_house2 -U_immLeft_N EOC
-ukranian_house4 -norwegian_house3 -U_immLeft_N EOC

-ukranian_house0 -spaniard_house2 -U_immLeft_S EOC
-ukranian_house0 -spaniard_house3 -U_immLeft_S EOC
-ukranian_house0 -spaniard_house4 -U_immLeft_S EOC
-ukranian_house1 -spaniard_house0 -U_immLeft_S EOC
-ukranian_house1 -spaniard_house3 -U_immLeft_S EOC
-ukranian_house1 -spaniard_house4 -U_immLeft_S EOC
-ukranian_house2 -spaniard_house0 -U_immLeft_S EOC
-ukranian_house2 -spaniard_house1 -U_immLeft_S EOC
-ukranian_house2 -spaniard_house4 -U_immLeft_S EOC
-ukranian_house3 -spaniard_house0 -U_immLeft_S EOC
-ukranian_house3 -spaniard_house1 -U_immLeft_S EOC
-ukranian_house3 -spaniard_house2 -U_immLeft_S EOC
-ukranian_house4 -spaniard_house0 -U_immLeft_S EOC
-ukranian_house4 -spaniard_house1 -U_immLeft_S EOC
-ukranian_house4 -spaniard_house2 -U_immLeft_S EOC
-ukranian_house4 -spaniard_house3 -U_immLeft_S EOC

/* Positive constraints about one house being next to another. */
-E_immLeft_J E_nextTo_J EOC
-E_immLeft_N E_nextTo_N EOC
-E_immLeft_S E_nextTo_S EOC
-E_immLeft_U E_nextTo_U EOC
-J_immLeft_N J_nextTo_N EOC
-J_immLeft_S J_nextTo_S EOC
-J_immLeft_U J_nextTo_U EOC
-N_immLeft_S N_nextTo_S EOC
-N_immLeft_U N_nextTo_U EOC
-S_immLeft_U S_nextTo_U EOC

-J_immLeft_E E_nextTo_J EOC
-N_immLeft_E E_nextTo_N EOC
-S_immLeft_E E_nextTo_S EOC
-U_immLeft_E E_nextTo_U EOC
-N_immLeft_J J_nextTo_N EOC
-S_immLeft_J J_nextTo_S EOC
-U_immLeft_J J_nextTo_U EOC
-S_immLeft_N N_nextTo_S EOC
-U_immLeft_N N_nextTo_U EOC
-U_immLeft_S S_nextTo_U EOC

/* Negative constraints about one house being next to another. */
E_immLeft_J J_immLeft_E -E_nextTo_J EOC
E_immLeft_N N_immLeft_E -E_nextTo_N EOC
E_immLeft_S S_immLeft_E -E_nextTo_S EOC
E_immLeft_U U_immLeft_E -E_nextTo_U EOC
J_immLeft_N N_immLeft_J -J_nextTo_N EOC
J_immLeft_S S_immLeft_J -J_nextTo_S EOC
J_immLeft_U U_immLeft_J -J_nextTo_U EOC
N_immLeft_S S_immLeft_N -N_nextTo_S EOC
N_immLeft_U U_immLeft_N -N_nextTo_U EOC
S_immLeft_U U_immLeft_S -S_nextTo_U EOC


/* =================================================================== */

/* Problem-specific constraints, listed in increasing order of
   complexity. */

/* Exactly one person lives in each location. */
-englishman_house0 -japanese_house0 EOC
-englishman_house0 -norwegian_house0 EOC
-englishman_house0 -spaniard_house0 EOC
-englishman_house0 -ukranian_house0 EOC
-japanese_house0 -norwegian_house0 EOC
-japanese_house0 -spaniard_house0 EOC
-japanese_house0 -ukranian_house0 EOC
-norwegian_house0 -spaniard_house0 EOC
-norwegian_house0 -ukranian_house0 EOC
-spaniard_house0 -ukranian_house0 EOC

-englishman_house1 -japanese_house1 EOC
-englishman_house1 -norwegian_house1 EOC
-englishman_house1 -spaniard_house1 EOC
-englishman_house1 -ukranian_house1 EOC
-japanese_house1 -norwegian_house1 EOC
-japanese_house1 -spaniard_house1 EOC
-japanese_house1 -ukranian_house1 EOC
-norwegian_house1 -spaniard_house1 EOC
-norwegian_house1 -ukranian_house1 EOC
-spaniard_house1 -ukranian_house1 EOC

-englishman_house2 -japanese_house2 EOC
-englishman_house2 -norwegian_house2 EOC
-englishman_house2 -spaniard_house2 EOC
-englishman_house2 -ukranian_house2 EOC
-japanese_house2 -norwegian_house2 EOC
-japanese_house2 -spaniard_house2 EOC
-japanese_house2 -ukranian_house2 EOC
-norwegian_house2 -spaniard_house2 EOC
-norwegian_house2 -ukranian_house2 EOC
-spaniard_house2 -ukranian_house2 EOC

-englishman_house3 -japanese_house3 EOC
-englishman_house3 -norwegian_house3 EOC
-englishman_house3 -spaniard_house3 EOC
-englishman_house3 -ukranian_house3 EOC
-japanese_house3 -norwegian_house3 EOC
-japanese_house3 -spaniard_house3 EOC
-japanese_house3 -ukranian_house3 EOC
-norwegian_house3 -spaniard_house3 EOC
-norwegian_house3 -ukranian_house3 EOC
-spaniard_house3 -ukranian_house3 EOC

-englishman_house4 -japanese_house4 EOC
-englishman_house4 -norwegian_house4 EOC
-englishman_house4 -spaniard_house4 EOC
-englishman_house4 -ukranian_house4 EOC
-japanese_house4 -norwegian_house4 EOC
-japanese_house4 -spaniard_house4 EOC
-japanese_house4 -ukranian_house4 EOC
-norwegian_house4 -spaniard_house4 EOC
-norwegian_house4 -ukranian_house4 EOC
-spaniard_house4 -ukranian_house4 EOC

/* Exactly one person lives in each house of a given color. */
-englishman_redHouse -japanese_redHouse EOC
-englishman_redHouse -norwegian_redHouse EOC
-englishman_redHouse -spaniard_redHouse EOC
-englishman_redHouse -ukranian_redHouse EOC
-japanese_redHouse -norwegian_redHouse EOC
-japanese_redHouse -spaniard_redHouse EOC
-japanese_redHouse -ukranian_redHouse EOC
-norwegian_redHouse -spaniard_redHouse EOC
-norwegian_redHouse -ukranian_redHouse EOC
-spaniard_redHouse -ukranian_redHouse EOC

-englishman_greenHouse -japanese_greenHouse EOC
-englishman_greenHouse -norwegian_greenHouse EOC
-englishman_greenHouse -spaniard_greenHouse EOC
-englishman_greenHouse -ukranian_greenHouse EOC
-japanese_greenHouse -norwegian_greenHouse EOC
-japanese_greenHouse -spaniard_greenHouse EOC
-japanese_greenHouse -ukranian_greenHouse EOC
-norwegian_greenHouse -spaniard_greenHouse EOC
-norwegian_greenHouse -ukranian_greenHouse EOC
-spaniard_greenHouse -ukranian_greenHouse EOC

-englishman_ivoryHouse -japanese_ivoryHouse EOC
-englishman_ivoryHouse -norwegian_ivoryHouse EOC
-englishman_ivoryHouse -spaniard_ivoryHouse EOC
-englishman_ivoryHouse -ukranian_ivoryHouse EOC
-japanese_ivoryHouse -norwegian_ivoryHouse EOC
-japanese_ivoryHouse -spaniard_ivoryHouse EOC
-japanese_ivoryHouse -ukranian_ivoryHouse EOC
-norwegian_ivoryHouse -spaniard_ivoryHouse EOC
-norwegian_ivoryHouse -ukranian_ivoryHouse EOC
-spaniard_ivoryHouse -ukranian_ivoryHouse EOC

-englishman_yellowHouse -japanese_yellowHouse EOC
-englishman_yellowHouse -norwegian_yellowHouse EOC
-englishman_yellowHouse -spaniard_yellowHouse EOC
-englishman_yellowHouse -ukranian_yellowHouse EOC
-japanese_yellowHouse -norwegian_yellowHouse EOC
-japanese_yellowHouse -spaniard_yellowHouse EOC
-japanese_yellowHouse -ukranian_yellowHouse EOC
-norwegian_yellowHouse -spaniard_yellowHouse EOC
-norwegian_yellowHouse -ukranian_yellowHouse EOC
-spaniard_yellowHouse -ukranian_yellowHouse EOC

-englishman_blueHouse -japanese_blueHouse EOC
-englishman_blueHouse -norwegian_blueHouse EOC
-englishman_blueHouse -spaniard_blueHouse EOC
-englishman_blueHouse -ukranian_blueHouse EOC
-japanese_blueHouse -norwegian_blueHouse EOC
-japanese_blueHouse -spaniard_blueHouse EOC
-japanese_blueHouse -ukranian_blueHouse EOC
-norwegian_blueHouse -spaniard_blueHouse EOC
-norwegian_blueHouse -ukranian_blueHouse EOC
-spaniard_blueHouse -ukranian_blueHouse EOC

/* Exactly one person has each kind of pet. */
-englishman_zebra -japanese_zebra EOC
-englishman_zebra -norwegian_zebra EOC
-englishman_zebra -spaniard_zebra EOC
-englishman_zebra -ukranian_zebra EOC
-japanese_zebra -norwegian_zebra EOC
-japanese_zebra -spaniard_zebra EOC
-japanese_zebra -ukranian_zebra EOC
-norwegian_zebra -spaniard_zebra EOC
-norwegian_zebra -ukranian_zebra EOC
-spaniard_zebra -ukranian_zebra EOC

-englishman_dog -japanese_dog EOC
-englishman_dog -norwegian_dog EOC
-englishman_dog -spaniard_dog EOC
-englishman_dog -ukranian_dog EOC
-japanese_dog -norwegian_dog EOC
-japanese_dog -spaniard_dog EOC
-japanese_dog -ukranian_dog EOC
-norwegian_dog -spaniard_dog EOC
-norwegian_dog -ukranian_dog EOC
-spaniard_dog -ukranian_dog EOC

-englishman_horse -japanese_horse EOC
-englishman_horse -norwegian_horse EOC
-englishman_horse -spaniard_horse EOC
-englishman_horse -ukranian_horse EOC
-japanese_horse -norwegian_horse EOC
-japanese_horse -spaniard_horse EOC
-japanese_horse -ukranian_horse EOC
-norwegian_horse -spaniard_horse EOC
-norwegian_horse -ukranian_horse EOC
-spaniard_horse -ukranian_horse EOC

-englishman_fox -japanese_fox EOC
-englishman_fox -norwegian_fox EOC
-englishman_fox -spaniard_fox EOC
-englishman_fox -ukranian_fox EOC
-japanese_fox -norwegian_fox EOC
-japanese_fox -spaniard_fox EOC
-japanese_fox -ukranian_fox EOC
-norwegian_fox -spaniard_fox EOC
-norwegian_fox -ukranian_fox EOC
-spaniard_fox -ukranian_fox EOC

-englishman_snails -japanese_snails EOC
-englishman_snails -norwegian_snails EOC
-englishman_snails -spaniard_snails EOC
-englishman_snails -ukranian_snails EOC
-japanese_snails -norwegian_snails EOC
-japanese_snails -spaniard_snails EOC
-japanese_snails -ukranian_snails EOC
-norwegian_snails -spaniard_snails EOC
-norwegian_snails -ukranian_snails EOC
-spaniard_snails -ukranian_snails EOC

/* Exactly one person has each kind of drink as a favorite. */
-englishman_coffee -japanese_coffee EOC
-englishman_coffee -norwegian_coffee EOC
-englishman_coffee -spaniard_coffee EOC
-englishman_coffee -ukranian_coffee EOC
-japanese_coffee -norwegian_coffee EOC
-japanese_coffee -spaniard_coffee EOC
-japanese_coffee -ukranian_coffee EOC
-norwegian_coffee -spaniard_coffee EOC
-norwegian_coffee -ukranian_coffee EOC
-spaniard_coffee -ukranian_coffee EOC

-englishman_tea -japanese_tea EOC
-englishman_tea -norwegian_tea EOC
-englishman_tea -spaniard_tea EOC
-englishman_tea -ukranian_tea EOC
-japanese_tea -norwegian_tea EOC
-japanese_tea -spaniard_tea EOC
-japanese_tea -ukranian_tea EOC
-norwegian_tea -spaniard_tea EOC
-norwegian_tea -ukranian_tea EOC
-spaniard_tea -ukranian_tea EOC

-englishman_orangeJuice -japanese_orangeJuice EOC
-englishman_orangeJuice -norwegian_orangeJuice EOC
-englishman_orangeJuice -spaniard_orangeJuice EOC
-englishman_orangeJuice -ukranian_orangeJuice EOC
-japanese_orangeJuice -norwegian_orangeJuice EOC
-japanese_orangeJuice -spaniard_orangeJuice EOC
-japanese_orangeJuice -ukranian_orangeJuice EOC
-norwegian_orangeJuice -spaniard_orangeJuice EOC
-norwegian_orangeJuice -ukranian_orangeJuice EOC
-spaniard_orangeJuice -ukranian_orangeJuice EOC

-englishman_water -japanese_water EOC
-englishman_water -norwegian_water EOC
-englishman_water -spaniard_water EOC
-englishman_water -ukranian_water EOC
-japanese_water -norwegian_water EOC
-japanese_water -spaniard_water EOC
-japanese_water -ukranian_water EOC
-norwegian_water -spaniard_water EOC
-norwegian_water -ukranian_water EOC
-spaniard_water -ukranian_water EOC

-englishman_milk -japanese_milk EOC
-englishman_milk -norwegian_milk EOC
-englishman_milk -spaniard_milk EOC
-englishman_milk -ukranian_milk EOC
-japanese_milk -norwegian_milk EOC
-japanese_milk -spaniard_milk EOC
-japanese_milk -ukranian_milk EOC
-norwegian_milk -spaniard_milk EOC
-norwegian_milk -ukranian_milk EOC
-spaniard_milk -ukranian_milk EOC

/* Exactly one person smokes each brand of cigarette. */
-englishman_oldGold -japanese_oldGold EOC
-englishman_oldGold -norwegian_oldGold EOC
-englishman_oldGold -spaniard_oldGold EOC
-englishman_oldGold -ukranian_oldGold EOC
-japanese_oldGold -norwegian_oldGold EOC
-japanese_oldGold -spaniard_oldGold EOC
-japanese_oldGold -ukranian_oldGold EOC
-norwegian_oldGold -spaniard_oldGold EOC
-norwegian_oldGold -ukranian_oldGold EOC
-spaniard_oldGold -ukranian_oldGold EOC

-englishman_parliament -japanese_parliament EOC
-englishman_parliament -norwegian_parliament EOC
-englishman_parliament -spaniard_parliament EOC
-englishman_parliament -ukranian_parliament EOC
-japanese_parliament -norwegian_parliament EOC
-japanese_parliament -spaniard_parliament EOC
-japanese_parliament -ukranian_parliament EOC
-norwegian_parliament -spaniard_parliament EOC
-norwegian_parliament -ukranian_parliament EOC
-spaniard_parliament -ukranian_parliament EOC

-englishman_kools -japanese_kools EOC
-englishman_kools -norwegian_kools EOC
-englishman_kools -spaniard_kools EOC
-englishman_kools -ukranian_kools EOC
-japanese_kools -norwegian_kools EOC
-japanese_kools -spaniard_kools EOC
-japanese_kools -ukranian_kools EOC
-norwegian_kools -spaniard_kools EOC
-norwegian_kools -ukranian_kools EOC
-spaniard_kools -ukranian_kools EOC

-englishman_lucky -japanese_lucky EOC
-englishman_lucky -norwegian_lucky EOC
-englishman_lucky -spaniard_lucky EOC
-englishman_lucky -ukranian_lucky EOC
-japanese_lucky -norwegian_lucky EOC
-japanese_lucky -spaniard_lucky EOC
-japanese_lucky -ukranian_lucky EOC
-norwegian_lucky -spaniard_lucky EOC
-norwegian_lucky -ukranian_lucky EOC
-spaniard_lucky -ukranian_lucky EOC

-englishman_chesterfield -japanese_chesterfield EOC
-englishman_chesterfield -norwegian_chesterfield EOC
-englishman_chesterfield -spaniard_chesterfield EOC
-englishman_chesterfield -ukranian_chesterfield EOC
-japanese_chesterfield -norwegian_chesterfield EOC
-japanese_chesterfield -spaniard_chesterfield EOC
-japanese_chesterfield -ukranian_chesterfield EOC
-norwegian_chesterfield -spaniard_chesterfield EOC
-norwegian_chesterfield -ukranian_chesterfield EOC
-spaniard_chesterfield -ukranian_chesterfield EOC


/* 1.  The Englishman lives in the red house. */
englishman_redHouse EOC

/* 2.  The Spaniard has a dog. */
spaniard_dog EOC

/* 3.  The Ukranian drinks tea. */
ukranian_tea EOC

/* 4.  The Norwegian lives in the leftmost house, i.e., house 0. */
norwegian_house0 EOC

/* 5.  The Japanese smokes Parliaments. */
japanese_parliament EOC

/* 6.  The Norwegian lives next to the blue house. */
-norwegian_blueHouse             EOC
-englishman_blueHouse E_nextTo_N EOC
-japanese_blueHouse   J_nextTo_N EOC
-spaniard_blueHouse   N_nextTo_S EOC
-ukranian_blueHouse   N_nextTo_U EOC

/* 7.  Coffee is drunk in the green house. */
-englishman_coffee -japanese_greenHouse  EOC
-englishman_coffee -norwegian_greenHouse EOC
-englishman_coffee -spaniard_greenHouse  EOC
-englishman_coffee -ukranian_greenHouse  EOC

-japanese_coffee -englishman_greenHouse EOC
-japanese_coffee -norwegian_greenHouse  EOC
-japanese_coffee -spaniard_greenHouse   EOC
-japanese_coffee -ukranian_greenHouse   EOC

-norwegian_coffee -englishman_greenHouse EOC
-norwegian_coffee -japanese_greenHouse   EOC
-norwegian_coffee -spaniard_greenHouse   EOC
-norwegian_coffee -ukranian_greenHouse   EOC

-spaniard_coffee -englishman_greenHouse EOC
-spaniard_coffee -japanese_greenHouse   EOC
-spaniard_coffee -norwegian_greenHouse  EOC
-spaniard_coffee -ukranian_greenHouse   EOC

-ukranian_coffee -englishman_greenHouse EOC
-ukranian_coffee -japanese_greenHouse   EOC
-ukranian_coffee -norwegian_greenHouse  EOC
-ukranian_coffee -spaniard_greenHouse   EOC

/* 8.  The snail owner smokes Old Gold. */
-englishman_snails -japanese_oldGold  EOC
-englishman_snails -norwegian_oldGold EOC
-englishman_snails -spaniard_oldGold  EOC
-englishman_snails -ukranian_oldGold  EOC

-japanese_snails -englishman_oldGold EOC
-japanese_snails -norwegian_oldGold  EOC
-japanese_snails -spaniard_oldGold   EOC
-japanese_snails -ukranian_oldGold   EOC

-norwegian_snails -englishman_oldGold EOC
-norwegian_snails -japanese_oldGold   EOC
-norwegian_snails -spaniard_oldGold   EOC
-norwegian_snails -ukranian_oldGold   EOC

-spaniard_snails -englishman_oldGold EOC
-spaniard_snails -japanese_oldGold   EOC
-spaniard_snails -norwegian_oldGold  EOC
-spaniard_snails -ukranian_oldGold   EOC

-ukranian_snails -englishman_oldGold EOC
-ukranian_snails -japanese_oldGold   EOC
-ukranian_snails -norwegian_oldGold  EOC
-ukranian_snails -spaniard_oldGold   EOC

/* 9.  The inhabitant of the yellow house smokes Kools. */
-englishman_yellowHouse -japanese_kools  EOC
-englishman_yellowHouse -norwegian_kools EOC
-englishman_yellowHouse -spaniard_kools  EOC
-englishman_yellowHouse -ukranian_kools  EOC

-japanese_yellowHouse -englishman_kools EOC
-japanese_yellowHouse -norwegian_kools  EOC
-japanese_yellowHouse -spaniard_kools   EOC
-japanese_yellowHouse -ukranian_kools   EOC

-norwegian_yellowHouse -englishman_kools EOC
-norwegian_yellowHouse -japanese_kools   EOC
-norwegian_yellowHouse -spaniard_kools   EOC
-norwegian_yellowHouse -ukranian_kools   EOC

-spaniard_yellowHouse -englishman_kools EOC
-spaniard_yellowHouse -japanese_kools   EOC
-spaniard_yellowHouse -norwegian_kools  EOC
-spaniard_yellowHouse -ukranian_kools   EOC

-ukranian_yellowHouse -englishman_kools EOC
-ukranian_yellowHouse -japanese_kools   EOC
-ukranian_yellowHouse -norwegian_kools  EOC
-ukranian_yellowHouse -spaniard_kools   EOC

/* 10. The Lucky Strikes smoker drinks orange juice. */
-englishman_lucky -japanese_orangeJuice  EOC
-englishman_lucky -norwegian_orangeJuice EOC
-englishman_lucky -spaniard_orangeJuice  EOC
-englishman_lucky -ukranian_orangeJuice  EOC

-japanese_lucky -englishman_orangeJuice EOC
-japanese_lucky -norwegian_orangeJuice  EOC
-japanese_lucky -spaniard_orangeJuice   EOC
-japanese_lucky -ukranian_orangeJuice   EOC

-norwegian_lucky -englishman_orangeJuice EOC
-norwegian_lucky -japanese_orangeJuice   EOC
-norwegian_lucky -spaniard_orangeJuice   EOC
-norwegian_lucky -ukranian_orangeJuice   EOC

-spaniard_lucky -englishman_orangeJuice EOC
-spaniard_lucky -japanese_orangeJuice   EOC
-spaniard_lucky -norwegian_orangeJuice  EOC
-spaniard_lucky -ukranian_orangeJuice   EOC

-ukranian_lucky -englishman_orangeJuice EOC
-ukranian_lucky -japanese_orangeJuice   EOC
-ukranian_lucky -norwegian_orangeJuice  EOC
-ukranian_lucky -spaniard_orangeJuice   EOC

/* 11. Milk is drunk in the middle house, i.e., house 2. */
-englishman_milk -japanese_house2  EOC
-englishman_milk -norwegian_house2 EOC
-englishman_milk -spaniard_house2  EOC
-englishman_milk -ukranian_house2  EOC

-japanese_milk -englishman_house2 EOC
-japanese_milk -norwegian_house2  EOC
-japanese_milk -spaniard_house2   EOC
-japanese_milk -ukranian_house2   EOC

-norwegian_milk -englishman_house2 EOC
-norwegian_milk -japanese_house2   EOC
-norwegian_milk -spaniard_house2   EOC
-norwegian_milk -ukranian_house2   EOC

-spaniard_milk -englishman_house2 EOC
-spaniard_milk -japanese_house2   EOC
-spaniard_milk -norwegian_house2  EOC
-spaniard_milk -ukranian_house2   EOC

-ukranian_milk -englishman_house2 EOC
-ukranian_milk -japanese_house2   EOC
-ukranian_milk -norwegian_house2  EOC
-ukranian_milk -spaniard_house2   EOC

/* 12. The green house is immediately to the right of the ivory house. */
-englishman_ivoryHouse -japanese_greenHouse  E_immLeft_J EOC
-englishman_ivoryHouse -norwegian_greenHouse E_immLeft_N EOC
-englishman_ivoryHouse -spaniard_greenHouse  E_immLeft_S EOC
-englishman_ivoryHouse -ukranian_greenHouse  E_immLeft_U EOC

-japanese_ivoryHouse -englishman_greenHouse J_immLeft_E EOC
-japanese_ivoryHouse -norwegian_greenHouse  J_immLeft_N EOC
-japanese_ivoryHouse -spaniard_greenHouse   J_immLeft_S EOC
-japanese_ivoryHouse -ukranian_greenHouse   J_immLeft_U EOC

-norwegian_ivoryHouse -englishman_greenHouse N_immLeft_E EOC
-norwegian_ivoryHouse -japanese_greenHouse   N_immLeft_J EOC
-norwegian_ivoryHouse -spaniard_greenHouse   N_immLeft_S EOC
-norwegian_ivoryHouse -ukranian_greenHouse   N_immLeft_U EOC

-spaniard_ivoryHouse -englishman_greenHouse S_immLeft_E EOC
-spaniard_ivoryHouse -japanese_greenHouse   S_immLeft_J EOC
-spaniard_ivoryHouse -norwegian_greenHouse  S_immLeft_N EOC
-spaniard_ivoryHouse -ukranian_greenHouse   S_immLeft_U EOC

-ukranian_ivoryHouse -englishman_greenHouse U_immLeft_E EOC
-ukranian_ivoryHouse -japanese_greenHouse   U_immLeft_J EOC
-ukranian_ivoryHouse -norwegian_greenHouse  U_immLeft_N EOC
-ukranian_ivoryHouse -spaniard_greenHouse   U_immLeft_S EOC

/* 13. The Chesterfield smoker lives next door to the fox owner. */
-englishman_chesterfield -englishman_fox EOC
-japanese_chesterfield   -japanese_fox   EOC
-norwegian_chesterfield  -norwegian_fox  EOC
-spaniard_chesterfield   -spaniard_fox   EOC
-ukranian_chesterfield   -ukranian_fox   EOC

-englishman_chesterfield -japanese_fox  E_nextTo_J EOC
-englishman_chesterfield -norwegian_fox E_nextTo_N EOC
-englishman_chesterfield -spaniard_fox  E_nextTo_S EOC
-englishman_chesterfield -ukranian_fox  E_nextTo_U EOC

-japanese_chesterfield -englishman_fox J_nextTo_E EOC
-japanese_chesterfield -norwegian_fox  J_nextTo_N EOC
-japanese_chesterfield -spaniard_fox   J_nextTo_S EOC
-japanese_chesterfield -ukranian_fox   J_nextTo_U EOC

-norwegian_chesterfield -englishman_fox N_nextTo_E EOC
-norwegian_chesterfield -japanese_fox   N_nextTo_J EOC
-norwegian_chesterfield -spaniard_fox   N_nextTo_S EOC
-norwegian_chesterfield -ukranian_fox   N_nextTo_U EOC

-spaniard_chesterfield -englishman_fox S_nextTo_E EOC
-spaniard_chesterfield -japanese_fox   S_nextTo_J EOC
-spaniard_chesterfield -norwegian_fox  S_nextTo_N EOC
-spaniard_chesterfield -ukranian_fox   S_nextTo_U EOC

-ukranian_chesterfield -englishman_fox U_nextTo_E EOC
-ukranian_chesterfield -japanese_fox   U_nextTo_J EOC
-ukranian_chesterfield -norwegian_fox  U_nextTo_N EOC
-ukranian_chesterfield -spaniard_fox   U_nextTo_S EOC

/* 14. The Kools smoker lives next door to where the horse is kept. */
-englishman_kools -englishman_horse EOC
-japanese_kools   -japanese_horse   EOC
-norwegian_kools  -norwegian_horse  EOC
-spaniard_kools   -spaniard_horse   EOC
-ukranian_kools   -ukranian_horse   EOC

-englishman_kools -japanese_horse  E_nextTo_J EOC
-englishman_kools -norwegian_horse E_nextTo_N EOC
-englishman_kools -spaniard_horse  E_nextTo_S EOC
-englishman_kools -ukranian_horse  E_nextTo_U EOC

-japanese_kools -englishman_horse J_nextTo_E EOC
-japanese_kools -norwegian_horse  J_nextTo_N EOC
-japanese_kools -spaniard_horse   J_nextTo_S EOC
-japanese_kools -ukranian_horse   J_nextTo_U EOC

-norwegian_kools -englishman_horse N_nextTo_E EOC
-norwegian_kools -japanese_horse   N_nextTo_J EOC
-norwegian_kools -spaniard_horse   N_nextTo_S EOC
-norwegian_kools -ukranian_horse   N_nextTo_U EOC

-spaniard_kools -englishman_horse S_nextTo_E EOC
-spaniard_kools -japanese_horse   S_nextTo_J EOC
-spaniard_kools -norwegian_horse  S_nextTo_N EOC
-spaniard_kools -ukranian_horse   S_nextTo_U EOC

-ukranian_kools -englishman_horse U_nextTo_E EOC
-ukranian_kools -japanese_horse   U_nextTo_J EOC
-ukranian_kools -norwegian_horse  U_nextTo_N EOC
-ukranian_kools -spaniard_horse   U_nextTo_S EOC