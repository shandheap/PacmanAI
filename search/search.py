# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

from copy import copy, deepcopy
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first and returns the first accepted path to the goal. This is implemented with a graph search algorithm.
    """
    
    fringe = util.Stack()
    paths = util.Stack()
    discovered = []
    fringe.push(problem.getStartState())
    paths.push([])
    
    while not fringe.isEmpty():
        current_state = fringe.pop()
        current_path = paths.pop()
        discovered.append(current_state)
        if problem.isGoalState(current_state)==True:
            return current_path
        children = problem.getSuccessors(current_state)
        for successor in children:
            if successor[0] not in discovered:
                copy = current_path[:]
                copy.append(successor[1])
                paths.push(copy)
                fringe.push(successor[0])
    return None

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first and returns the shortest possible accepted path. This is implemented with a graph search algorithm.
    """
    fringe = util.Queue()
    paths = util.Queue()
    discovered = []
    fringe.push(problem.getStartState())
    paths.push([])
    
    while not fringe.isEmpty():
        current_state = fringe.pop()
        current_path = paths.pop()
        discovered.append(deepcopy(current_state))          # Makes a deep copy so that the entry in list discovered is not altered by changes to current_state
        if problem.isGoalState(current_state)==True:
            return current_path
        children = problem.getSuccessors(current_state)
        for successor in children:
            if successor[0] not in discovered:
                if type(successor[0][0]) == tuple and successor[0][0] in problem.corners:
                    if problem.corners[problem.current_corner] == successor[0][0]:
                        if problem.goal[problem.current_corner] == False:
                            problem.goal[problem.current_corner] = True
                            fringe = util.Queue()
                            paths = util.Queue()
                            problem.current_corner += 1
                discovered.append(deepcopy(successor[0]))
                copy = current_path[:]
                copy.append(successor[1])
                paths.push(copy)
                fringe.push(successor[0])
    return None

def uniformCostSearch(problem):
    "Search the node of least total cost first and returns the shortest possible accepted path. This is implemented with a graph search algorithm."
    
    fringe = util.PriorityQueue()
    paths = util.PriorityQueue()
    costs = util.PriorityQueue()
    discovered = []
    fringe.push(problem.getStartState(), 0)
    paths.push([], 0)
    costs.push(0, 0)
    
    while not fringe.isEmpty():
        current_state = fringe.pop()
        current_path = paths.pop()
        cost = costs.pop()
        discovered.append(current_state)
        if problem.isGoalState(current_state)==True:
            return current_path
        children = problem.getSuccessors(current_state)
        for successor in children:
            if successor[0] not in discovered:
                copy = current_path[:]
                copy.append(successor[1])
                costs.push(successor[2] + cost, successor[2] + cost)
                paths.push(copy, successor[2] + cost)
                fringe.push(successor[0], successor[2] + cost)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic = nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    
    fringe = util.PriorityQueue()
    paths = util.PriorityQueue()
    aStarCosts = util.PriorityQueue()
    discovered = []
    heuristicCost = heuristic(problem.getStartState(), problem)
    fringe.push(problem.getStartState(), heuristicCost)
    paths.push([], heuristicCost)
    aStarCosts.push(heuristicCost, heuristicCost)
    
    while not fringe.isEmpty():
        current_state = fringe.pop()
        current_path = paths.pop()
        cost = aStarCosts.pop()
        while current_state in discovered:
            current_state = fringe.pop()
            current_path = paths.pop()
            cost = aStarCosts.pop()
        discovered.append(deepcopy(current_state))              # Makes a deep copy so that the entry in list discovered is not altered by changes to current_state
        if problem.isGoalState(current_state)==True:
            return current_path
        children = problem.getSuccessors(current_state)
        for successor in children:
            if successor[0] not in discovered:
                if type(successor[0][0]) == tuple and successor[0][0] in problem.corners:
                    if problem.corners[problem.current_corner] == successor[0][0]:
                        if problem.goal[problem.current_corner] == successor[0][0]:
                            problem.goal[problem.current_corner] = True
                            fringe = util.PriorityQueue()
                            paths = util.PriorityQueue()
                            aStarCosts = util.PriorityQueue()
                            problem.current_corner += 1
                copy = current_path[:]
                copy.append(successor[1])
                heuristicCost = heuristic(successor[0], problem)
                aStarCosts.push(successor[2] + cost, successor[2] + cost + heuristicCost)
                paths.push(copy, successor[2] + cost + heuristicCost)
                fringe.push(successor[0], successor[2] + cost + heuristicCost)
    return None



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
