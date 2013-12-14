To perform the follow functions, the repository must be copied to your local machine and then cd with terminal to the folder search. Files that were modified by me are search.py and searchAgents.py.

There are several different search algorithms that I have implemented here in python code which can be executed as follows:

Search
==========

To perform the follow functions, the repository must be copied to your local machine and then cd with terminal to the folder search. File edited by me was search.py and searchAgents.py.

Depth-First Search
==================

Terminal Command - python pacman.py -l bigMaze -z .5 -p SearchAgent

This searches through the entire maze using a Depth-First Search algorithm to find a acceptable path to a food pellet.

Breadth-First Search
====================

Terminal Command - python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5

This searches through the entire maze using a Breadth-First Search algorithm to find the shortest path to a food pellet.

Uniform-First Search
====================

Terminal Command - python pacman.py -l mediumScaryMaze -p StayWestSearchAgent

This searches through the entire maze using a Uniform Cost Search algorithm to find the least cost path to a food pellet, where costly paths are dictated by ghost circulating areas.

A* Search
=========

Terminal Command - python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

This searches through the entire maze using a A* Search algorithm to find the least cost path to a food pellet, much faster than Breadth-FIrst Search because of enhanced heuristics.

Search for the shortest path through all the food pellets
=========================================================

Terminal Command - python pacman.py -l trickySearch -p AStarFoodSearchAgent

Additional Maze Configuration - python pacman.py -l tinySearch -p AStarFoodSearchAgent

This searches through the entire maze using a Minimal Spanning Tree algorithm to find the least cost path through all the food pellets, much faster than Breadth-FIrst Search because of enhanced heuristics.

Search for the path through all the food pellets
================================================

Terminal Command - python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5 

This uses a Greedy-Search Principle as it tries to eat the closest food pellet until there are none left.

Multiagent
==========

To perform the follow functions, the repository must be copied to your local machine and then cd with terminal to the folder multiagent. File edited by me was multiAgents.py.

Search for the path through all the food pellets while avoiding the enemy agent
===============================================================================

Terminal Commands - python pacman.py -p ReflexAgent -l testClassic
					python pacman.py -p ReflexAgent -l openClassic

This uses an evaluation function to computer minimum spanning trees across all food pellets, and when pacman is close to his adversary, he changes his algorithm to become more prudent and avoid the enemy.
