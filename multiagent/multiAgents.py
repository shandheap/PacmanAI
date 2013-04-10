# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import copy
import sys

from game import Agent

def euclideanFunction(position1, position2):
    '''
    Returns the euclidean distance between two points

    Author - Shandheap Shanmuganathan
    '''
    xy1 = position1
    xy2 = position2
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

class DisjointSets:
    """
    This class is a representation of Disjoint sets in python.
    Use: In implementing Kruskal's algorithm for minimum spanning
         trees. This algorithm is used to find the shortest path 
         through all the food pellets.

    Author - Shandheap Shanmuganathan
    """
    #Class to represent each set
    class Set:
        #Private attributes
        __label = None
        #Public attributes
        rank = None
        parent = None
        #Public methods
        def __init__(self, label_value):
            self.__label = label_value
            self.rank = 0
            self.parent = self
        def getLabel(self):
            return self.__label

    #DisjointSets Private attributes
    __sets = None

    #DisjointSets Constructors and public methods.
    def __init__(self):
        self.__sets = {}

    def makeSet(self, label):
        if label in self.__sets: 
            return False         
        self.__sets[label] = self.Set(label)

    #Pre: 'labelA' and 'labelB' are labels or existing disjoint sets.
    def join(self, labelA, labelB):
        a = self.__sets.get(labelA)
        b = self.__sets.get(labelB)
        pa = self.find(a)
        pb = self.find(b)
        if pa == pb:
            return #They are already joined
        elif pa.rank > pb.rank:
            parent = pa
            child = pb
        elif pa.rank < pb.rank:
            parent = pb
            child = pa
        else:
            parent = pb
            child = pa
            parent.rank += 1
        child.parent = parent

    def find(self,x):
        if x == x.parent:
            return x
        pointer = copy.copy(x)
        while pointer != pointer.parent:
            pointer = pointer.parent
        return pointer

    def findLabel(self, label):
        return self.find(self.__sets.get(label))

    def __str__(self):
        return str(self.__sets)

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.

        Just like in the as before, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Author - Shandheap Shanmuganathan
        """

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        position, foodGrid = newPos, newFood
        foodPositions = foodGrid.asList()
        mstSum = 0
        forest = DisjointSets()
        edgeQueue = util.PriorityQueue()
        distancesToFood = []
        distancesToGhosts = []
        for foodLocation in foodPositions:
            positionToFoodlocation = euclideanFunction(position, foodLocation)
            distancesToFood.append(positionToFoodlocation)
            forest.makeSet(foodLocation)
        for otherFood in foodPositions:
            if foodLocation != otherFood:
                distance = abs(foodLocation[0] - otherFood[0]) + abs(foodLocation[1] - otherFood[1])
                edgeQueue.push((foodLocation, otherFood, distance), distance)
        while not edgeQueue.isEmpty():
            edge = edgeQueue.pop()
            if forest.findLabel(edge[0]) != forest.findLabel(edge[1]):
                mstSum += edge[2]
                forest.join(edge[0], edge[1])
        # Finds all the distances from current position to ghosts.
        for ghost_pos in successorGameState.getGhostPositions():
          distancesToGhosts.append(abs(position[0] - ghost_pos[0]) + abs(position[1] - ghost_pos[1]))
        if distancesToFood != []:
            minDistance = min(distancesToFood)
        else:
            minDistance = 0
        if min(distancesToGhosts) > 2:
          return successorGameState.getScore() - mstSum - minDistance
        return successorGameState.getScore() - mstSum - minDistance - min(distancesToGhosts) * abs(successorGameState.getScore())

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Minimax agent 
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        
        Author - Shandheap Shanmuganathan
        """

         # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        scores = []
        # Choose one of the best actions
        for action in legalMoves:
          successorGameState = gameState.generateSuccessor(0, action)
          scores.append(self.miniMax(successorGameState, 0, 1))
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print scores
        return legalMoves[chosenIndex]

    def maxAgent(self, gameState, currentDepth):
        '''
        Agent for the pacman AI.
        Author - Shandheap Shanmuganathan
        '''
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(0)
        v = - 1 - sys.maxint
        for action in legalMoves:
          successorGameState = gameState.generateSuccessor(0, action)
          v = max(v, self.miniMax(successorGameState, currentDepth, 1))
        # bestIndices = [index for index in range(len(scores)) if scores[index] == v]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print scores
        return v

    def minAgent(self, gameState, currentDepth, enemyID):
        '''
        Agent for the enemy AI.
        Author - Shandheap Shanmuganathan
        '''

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(enemyID)
        v = sys.maxint
        for action in legalMoves:
          successorGameState = gameState.generateSuccessor(enemyID, action)
          v = min(v, self.miniMax(successorGameState, currentDepth, 0))
        # bestIndices = [index for index in range(len(scores)) if scores[index] == v]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print scores
        return v

    def miniMax(self, gameState, currentDepth, playerID):
        '''
        Algorithm to find the minimax value at gameState, with limiter
        self.depth as the maximum depth recursion.

        Author - Shandheap Shanmuganathan
        '''
        if self.depth == currentDepth or gameState.isWin() or len(gameState.getLegalActions(0)) == 0 or gameState.isLose():
          return self.evaluationFunction(gameState)
        if playerID == 0:
          return self.maxAgent(gameState, currentDepth)
        
        numOfAgents = gameState.getNumAgents()
        enemyScores = 0
        currentDepth += 1
        tempState = gameState
        for agentID in range(numOfAgents - 1):
            legalMoves = tempState.getLegalActions(agentID + 1)
            # Enemy chooses one of the best actions
            scores = [self.miniMax(tempState, currentDepth, agentID) for action in legalMoves]
            enemyScores = self.minAgent(gameState, currentDepth, agentID + 1)
            bestIndices = [index for index in range(len(scores)) if scores[index] == enemyScores]
            chosenIndex = random.choice(bestIndices) # Pick randomly among the best
            tempState = gameState.generateSuccessor(agentID, legalMoves[chosenIndex])
        return enemyScores

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning 
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent 
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

    """
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        util.raiseNotDefined()

