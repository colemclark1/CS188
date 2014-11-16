# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        x,y = newPos
        score = 0.0
        # if newFood.asList() > 0:

        if newPos in successorGameState.getGhostPositions():
          return -9999

        closest_food_dist = 9999999
        for food in newFood.asList():
          closest_food_dist = min(closest_food_dist, abs(x-food[0]) + abs(y-food[1]))

        min_ghost_dist = 999999999
        for ghostPos in successorGameState.getGhostPositions():
          min_ghost_dist = min(min_ghost_dist, abs(x-ghostPos[0]) + abs(y-ghostPos[1]))

        score -= 16/float(min_ghost_dist**3+1)
        score += 4/float(closest_food_dist**2+1)
        score += 3/float(len(newFood.asList())+1)

        if(len(currentGameState.getFood().asList()) != len(newFood.asList())):
          score += 10

        if(min_ghost_dist == 1):
            score -= 5

        print(score)
        return score
        # return successorGameState.getScore()

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
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

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
      Your minimax agent (question 7)
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
        value, actions = self.minimaxHelper(gameState, self.depth, (), gameState.getNumAgents(), 0)
        if actions:
          return actions[-1]


    def minimaxHelper(self, cur_state, depth, curr_actions, numAgents, count):
        agentNum = count % numAgents
        maximizer = True if (agentNum == 0) else False

        if depth == 0 or len(cur_state.getLegalActions(count % numAgents)) == 0:
          return (self.evaluationFunction(cur_state), curr_actions)

        if agentNum == numAgents-1:
          depth -= 1

        if maximizer:
          valuesWithAction = []
          for action in cur_state.getLegalActions(agentNum):
            value, actions = self.minimaxHelper(cur_state.generateSuccessor(agentNum,action), depth, curr_actions, numAgents, count + 1,)
            actions += (action,)
            valuesWithAction.append((value, actions ))
          valuesWithAction = sorted(valuesWithAction, key=lambda x: x[0]) 
          return valuesWithAction[-1]
        else:
          valuesWithAction = []
          for action in cur_state.getLegalActions(agentNum):
            value, actions = self.minimaxHelper(cur_state.generateSuccessor(agentNum,action), depth, curr_actions, numAgents, count + 1,)
            actions += (action,)
            valuesWithAction.append((value, actions ))
          valuesWithAction = sorted(valuesWithAction, key=lambda x: x[0]) 
          return valuesWithAction[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        value, actions = self.expectimaxHelper(gameState, self.depth, (), gameState.getNumAgents(), 0)
        if actions:
          return actions[-1]

    def expectimaxHelper(self, cur_state, depth, curr_actions, numAgents, count):
        agentNum = count % numAgents
        maximizer = True if (agentNum == 0) else False

        if depth == 0 or len(cur_state.getLegalActions(count % numAgents)) == 0:
          return (self.evaluationFunction(cur_state), curr_actions)

        if agentNum == numAgents-1:
          depth -= 1

        if maximizer:
          valuesWithAction = []
          for action in cur_state.getLegalActions(agentNum):
            value, actions = self.expectimaxHelper(cur_state.generateSuccessor(agentNum,action), depth, curr_actions, numAgents, count + 1,)
            actions += (action,)
            valuesWithAction.append((value, actions ))
          valuesWithAction = sorted(valuesWithAction, key=lambda x: x[0]) 
          return valuesWithAction[-1]
        else:
          valuesWithAction = []
          for action in cur_state.getLegalActions(agentNum):
            value, actions = self.expectimaxHelper(cur_state.generateSuccessor(agentNum,action), depth, curr_actions, numAgents, count + 1,)
            actions += (action,)
            valuesWithAction.append((value, actions ))
          ave_value = sum([value[0] for value in valuesWithAction])/float(len(valuesWithAction))
          return (ave_value, ('Ghost Action',))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    moves = currentGameState.getLegalActions()
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodList = food.asList()
    foodCount = len(foodList)
    capsuleList = currentGameState.getCapsules()
    capsuleCount = len(capsuleList)
    ghostStates = currentGameState.getGhostStates()
    ghostPositions = currentGameState.getGhostPositions()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    x, y = currentGameState.getPacmanPosition()


    closest_food_dist = 9999999
    for food in food.asList():
      closest_food_dist = min(closest_food_dist, abs(x-food[0]) + abs(y-food[1]))

    score = currentGameState.getScore()*10
    closest_capsule_dist = 9999999
    for food in capsuleList:
      closest_capsule_dist = min(closest_capsule_dist, abs(x-food[0]) + abs(y-food[1]))
    score += 1000/(closest_capsule_dist**3 + 0.01)

    ghost_score = 0
    closest_ghost_distance = 99999999
    for idx,ghostState in enumerate(ghostStates):
      ghostPos = ghostState.getPosition()
      distance = abs(x-ghostPos[0]) + abs(y-ghostPos[1])
      if(scaredTimes[idx] > distance):
        score += 10000/distance**5
      if scaredTimes[idx] < distance:
        closest_ghost_distance = min(closest_ghost_distance, abs(x-ghostPos[0]) + abs(y-ghostPos[1]))

    score += 75.0/float(capsuleCount+.1)
    score -= 5/float(closest_ghost_distance**3+.1)
    foodscore = 10000.0/float(foodCount**.5+.1)
    score += foodscore
    score += 50/float(closest_food_dist+.1)

    if(foodCount==0):
      score += 9999999

    if(closest_ghost_distance < 3):
        run_score= 50000/(closest_ghost_distance**0.5 + 0.01)
        score -= run_score

    return score


# Abbreviation
better = betterEvaluationFunction

