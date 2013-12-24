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
    "The Euclidean distance function for two points."
    xy1 = position1
    xy2 = position2
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

class DisjointSets:

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
        #ret = ""
        #for e in self.__sets:
        #    ret = ret + "parent("+self.__sets[e].getLabel().__str__()+") = "+self.findLabel(e).parent.getLabel().__str__() + "\n"
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
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
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
      Minimax agent (question 2)
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
        legalMoves = gameState.getLegalActions(0)
        scores = []
        # Choose one of the best actions
        for move in legalMoves:
            successorGameState = gameState.generateSuccessor(0, move)
            scores.append(self.value(successorGameState, 1, 0))
        bestScore = max(scores)
        bestIndices = []
        for index in range(len(scores)):
            if scores[index] == bestScore:
                bestIndices.append(index)
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def value(self, gameState, agent, currentDepth):
        if self.depth == currentDepth or gameState.isWin() or len(gameState.getLegalActions(0)) == 0 or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if agent == 0:
            return self.max_value(gameState, currentDepth)
        else:
            return self.min_value(gameState, agent, currentDepth)

    def max_value(self, gameState, currentDepth):
        v = - sys.maxint - 1
        legalMoves = gameState.getLegalActions(0)
        for move in legalMoves:
            v = max(v, self.value(gameState.generateSuccessor(0, move), 1, currentDepth))
        return v

    def min_value(self, gameState, agent, currentDepth):
        v = sys.maxint
        if agent == gameState.getNumAgents():
            currentDepth += 1
            return self.value(gameState, 0, currentDepth)
        legalMoves = gameState.getLegalActions(agent)
        for move in legalMoves:
            v = min(v, self.value(gameState.generateSuccessor(agent, move), agent+1, currentDepth))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
         # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(0)
        scores = []
        # Initialize alpha and beta
        alpha = - sys.maxint - 1
        beta = sys.maxint
        # Choose one of the best actions
        for move in legalMoves:
            successorGameState = gameState.generateSuccessor(0, move)
            result = self.value(successorGameState, 1, 0, alpha, beta)
            scores.append(result[0])
            alpha = result[1]
            beta = result[2]
        bestScore = max(scores)
        bestIndices = []
        for index in range(len(scores)):
            if scores[index] == bestScore:
                bestIndices.append(index)
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]

    def value(self, gameState, agent, currentDepth, alpha, beta):
        if self.depth == currentDepth or gameState.isWin() or len(gameState.getLegalActions(0)) == 0 or gameState.isLose():
            return [self.evaluationFunction(gameState), alpha, beta]
        
        if agent == 0:
            return self.max_value(gameState, currentDepth, alpha, beta)
        else:
            return self.min_value(gameState, agent, currentDepth, alpha, beta)

    def max_value(self, gameState, currentDepth, alpha, beta):
        v = - sys.maxint - 1
        legalMoves = gameState.getLegalActions(0)
        for move in legalMoves:
            result = self.value(gameState.generateSuccessor(0, move),
                         1, currentDepth, alpha, beta)
            v = max(v, result[0])
            alpha = max(alpha, result[1])
            if v >= beta: return [v, alpha, beta]
            alpha = max(alpha, v)
        beta = min(beta, alpha)
        return [v, alpha, beta]

    def min_value(self, gameState, agent, currentDepth, alpha, beta):
        v = sys.maxint
        if agent == gameState.getNumAgents():
            currentDepth += 1
            return self.value(gameState, 0, currentDepth, alpha, beta)
        legalMoves = gameState.getLegalActions(agent)
        for move in legalMoves:
            result = self.value(gameState.generateSuccessor(agent, move),
                         agent+1, currentDepth, alpha, beta)
            v = min(v, result[0])
            beta = min(beta, result[2])
            if v <= alpha: return [v, alpha, beta]
            beta = min(beta, v)
        alpha = max(alpha, beta)
        return [v, alpha, beta]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

