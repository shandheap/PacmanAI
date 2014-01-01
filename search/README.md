#Search

Depth-First Search
==================

Terminal Command: 

`python pacman.py -l bigMaze -z .5 -p SearchAgent`

This searches through the entire maze using a Depth-First Search algorithm to find a acceptable path to a food pellet.

Breadth-First Search
====================

Terminal Command:

`python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5`

This searches through the entire maze using a Breadth-First Search algorithm to find the shortest path to a food pellet.

Uniform-First Search
====================

Terminal Command:

`python pacman.py -l mediumScaryMaze -p StayWestSearchAgent`

This searches through the entire maze using a Uniform Cost Search algorithm to find the least cost path to a food pellet, where costly paths are dictated by ghost circulating areas.

A* Search
=========

Terminal Command:

`python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`

This searches through the entire maze using a A* Search algorithm to find the least cost path to a food pellet, much faster than Breadth-FIrst Search because of enhanced heuristics.

Shortest Path Search
====================

Terminal Command:

`python pacman.py -l trickySearch -p AStarFoodSearchAgent`

Additional Maze Configuration: 

`python pacman.py -l tinySearch -p AStarFoodSearchAgent`

This searches through the entire maze using a Minimum Spanning Tree algorithm (Kruskal's algorithm) to find the least cost path through all the food pellets, much faster than Breadth-FIrst Search because of enhanced heuristics.

Greedy Path Search
==================

Terminal Command:

`python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5`

This uses a Greedy-Search Principle as it tries to eat the closest food pellet until there are none left.
