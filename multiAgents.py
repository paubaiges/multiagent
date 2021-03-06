# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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

        "Add more of your code here if you want to"

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

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Being close to the closest ghost will be bad (+4)
        closestGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        # Being close to the closest food will be great (-4)
        # Having no more food will be very perfect (-1000)
        closestFood = min([manhattanDistance(newPos, food) for food in newFood]) if newFood else -1000

        # How less food better
        food_size = len(newFood)

        return (-4)*closestFood + (-80)*food_size + (4)*closestGhost



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
      Your minimax agent (question 2)
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
        """
        "*** YOUR CODE HERE ***"

        def minim(gameState, depth, agentcounter):
            minimum = ["", float("inf")]
            ghostActions = gameState.getLegalActions(agentcounter)

            if ghostActions == 0:
                return self.evaluationFunction(gameState)
            else:
              for action in ghostActions:
                  currentState = gameState.generateSuccessor(agentcounter, action)
                  current = minimax(currentState, depth, agentcounter + 1)
                  if type(current) is not list:
                      newValue = current
                  else:
                      newValue = current[1]
                  if newValue < minimum[1]:
                      minimum = [action, newValue]
              return minimum

        def maxim(gameState, depth, agentcounter):
            maximum = ["", -float("inf")]
            ghostActions = gameState.getLegalActions(agentcounter)

            if ghostActions == 0:
                return self.evaluationFunction(gameState)
            else:
              for action in ghostActions:
                  currentState = gameState.generateSuccessor(agentcounter, action)
                  current = minimax(currentState, depth, agentcounter + 1)
                  if type(current) is not list:
                      newValue = current
                  else:
                      newValue = current[1]
                  if newValue > maximum[1]:
                      maximum = [action, newValue]
              return maximum


        def minimax(gameState, depth, agentcounter):
            if agentcounter >= gameState.getNumAgents():
                depth += 1
                agentcounter = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            else:
              if (agentcounter == 0):
                return maxim(gameState, depth, agentcounter)
              else:
                return minim(gameState, depth, agentcounter)

        actionsList = minimax(gameState, 0, 0)
        return actionsList[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "* YOUR CODE HERE *"
        return self.maxval(gameState, 0, 0, -float("inf"), float("inf"))[0]

    def alphabeta(self, gameState, agentIndex, depth, alpha, beta):
        if depth is self.depth * gameState.getNumAgents() \
                or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex is 0:
            return self.maxval(gameState, agentIndex, depth, alpha, beta)[1]
        else:
            return self.minval(gameState, agentIndex, depth, alpha, beta)[1]

    def maxval(self, gameState, agentIndex, depth, alpha, beta):
        bestAction = ("max",-float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            succAction = (action,self.alphabeta(gameState.generateSuccessor(agentIndex,action),
                                      (depth + 1)%gameState.getNumAgents(),depth+1, alpha, beta))
            bestAction = max(bestAction,succAction,key=lambda x:x[1])

            # Prunning
            if bestAction[1] > beta: return bestAction
            else: alpha = max(alpha,bestAction[1])

        return bestAction

    def minval(self, gameState, agentIndex, depth, alpha, beta):
        bestAction = ("min",float("inf"))
        for action in gameState.getLegalActions(agentIndex):
            succAction = (action,self.alphabeta(gameState.generateSuccessor(agentIndex,action),
                                      (depth + 1)%gameState.getNumAgents(),depth+1, alpha, beta))
            bestAction = min(bestAction,succAction,key=lambda x:x[1])

            # Prunning
            if bestAction[1] < alpha: return bestAction
            else: beta = min(beta, bestAction[1])

        return bestAction

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
        action, score = self.expectimax(self.depth, 0, gameState)
        return action

    def expectimax(self, depth, agent, state):
        if agent >= state.getNumAgents():
            agent = 0
            depth -= 1
            
        if not depth:
            return None, self.evaluationFunction(state)

        best = None, None # Action, Score
        for action in state.getLegalActions(agent):
            next_state = state.generateSuccessor(agent, action)

            next_action, next_score = self.expectimax(depth, agent+1, next_state)
            best_score = best[1]

            # Init best score in first iteration
            if best_score is None:
                if agent == 0:
                    best = action, next_score
                if agent != 0:
                    best_score = 0.0

            # Compare new action score
            if agent == 0: # Pacman maximazes
                if next_score > best_score:
                    best = action, next_score
            else: # Ghost minimizes
                ghostActions = state.getLegalActions(agent)
                if len(ghostActions) is not 0:
                    prob = 1.0 / len(ghostActions)
                best = action, best_score + prob * next_score
                
        if best == (None, None): # If no actions found
            return None, self.evaluationFunction(state)
            
        return best 

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman_position = list(currentGameState.getPacmanPosition())
    food_position = currentGameState.getFood().asList()
    food_list = []

    for food in food_position:
        distance = manhattanDistance(pacman_position, food)
        food_list.append(-1 * distance)

    if not food_list:
        food_list.append(0)

    return currentGameState.getScore() + max(food_list)

# Abbreviation
better = betterEvaluationFunction
