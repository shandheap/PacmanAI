#Multiagent

Reflex Agent
============

Terminal Command: 

`python pacman.py -p ReflexAgent -l testClassic`

This uses an evaluation function to computer minimum spanning trees across all food pellets, and when pacman is close to his adversary, he changes his algorithm to become more prudent and avoid the enemy.


Minimax Agent
=============

Terminal Command:

`python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4`

The program can optimize for the different possible situations pacman will be in, and will return the best one. (This assumes the ghosts are trying to kill pacman but in the demo they are random, otherwise pacman would have to expand a massive decision tree which will take too long.

Alpha-Beta Pruning
==================

Terminal Command:

`python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic`

This is an optimized version of the Minimax Agent that can evaluate moves faster.

Expectimax Agent
================

Terminal Command:

`python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3`

This is a variation of minimax where pacman realizes that the ghosts take random moves, rather than actively chasing pacman.