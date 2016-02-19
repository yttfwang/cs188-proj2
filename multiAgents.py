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
        newFood = successorGameState.getFood()
        minFoodDist = 1E9
        minGhostDist = 1E9
        for x in range(newFood.width):
          for y in range(newFood.height):
            if newFood[x][y]:
              foodManDist = abs(x - newPos[0]) + abs(y - newPos[1])
              
              if foodManDist < minFoodDist:
                minFoodDist = foodManDist
        invMinFoodDist = 1.0 / minFoodDist
        newGhostStates = successorGameState.getGhostStates()
        numAgents = successorGameState.getNumAgents()
        
        for i in range(1, numAgents):
          ghostPos = successorGameState.getGhostPosition(i)
          ghostManDist = abs(ghostPos[0] - newPos[0]) + abs(ghostPos[1] - newPos[1])
          if ghostManDist < minGhostDist:
            minGhostDist = ghostManDist
        invMinGhostDist = 1.0 / minGhostDist
       
        "*** YOUR CODE HERE ***"
        if minGhostDist < 3:
          invMinGhostDist = invMinGhostDist * 100
        totalScore = successorGameState.getScore() + invMinFoodDist - invMinGhostDist 
        #
        #print totalScore
        return totalScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    #print currentGameState.getScore()
    # print "GETSCORE"
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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        finalLevel = gameState.getNumAgents() * self.depth 

        def minimax(game_state, level):
          agentIndex = level % gameState.getNumAgents()
          if level >= finalLevel:
            print "Error with minimax function: levels_left should not be <= 0."
            return None
          
          elif level == finalLevel - 1: # must be a ghost, minimizer
            bestAction = ''
            lowestEvalNum = 999999
            #evalNum = -999999
            
            for action in game_state.getLegalActions(agentIndex):
              newState = game_state.generateSuccessor(agentIndex, action)
              

              evalNum = self.evaluationFunction(newState)

              if evalNum < lowestEvalNum:
                lowestEvalNum = evalNum
                bestAction = action
            
            #pdb.set_trace()
            #print "@@@1: level: ", level, ";  agentIndex: ", agentIndex, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@2: best eval, action: ", lowestEvalNum, bestAction
            return (lowestEvalNum, bestAction)
          
          elif level % gameState.getNumAgents() == 0: #Pacman's turn, maximizer
            bestAction = 'Stop'
            highestEvalNum = -999999
            #evalNum = -999999
            
            for action in game_state.getLegalActions(agentIndex):
              newState = game_state.generateSuccessor(agentIndex, action)
              
              if newState.isWin() or newState.isLose():
                evalNum = self.evaluationFunction(newState)
              else:
                #pdb.set_trace()
                evalNum , _ = minimax(newState, level + 1)

              if evalNum > highestEvalNum:
                highestEvalNum = evalNum
                bestAction = action
            
            #pdb.set_trace()
            #print "@@@ 3: level: ", level, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@ 4: highest eval, action: ", highestEvalNum, bestAction
            return (highestEvalNum, bestAction)

          else: #Ghosts' turn, minimizer
            bestAction = 'Stop'
            lowestEvalNum = 999999
            #evalNum = 999999
            
            for action in game_state.getLegalActions(agentIndex):
              newState = game_state.generateSuccessor(agentIndex, action)
              
              if newState.isWin() or newState.isLose():
                evalNum = self.evaluationFunction(newState)
              else:
                #pdb.set_trace()
                evalNum , _ = minimax(newState, level + 1)

              if evalNum < lowestEvalNum:
                lowestEvalNum = evalNum
                bestAction = action
            
            #pdb.set_trace()
            #print "@@@  5: level: ", level, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@  6: lowest eval, action: ", lowestEvalNum, bestAction
            return (lowestEvalNum, bestAction)


        

        evalNum , action = minimax(gameState, 0) #initially starts the level at 0
        #print "evalnum is:", evalNum
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        finalLevel = gameState.getNumAgents() * self.depth 

        def alphabeta(game_state, level, bestMin, bestMax):
          agentIndex = level % gameState.getNumAgents()
          if level >= finalLevel:
            # print "Error with minimax function: levels_left should not be <= 0."
            return None
          
          elif level == finalLevel - 1: # must be a ghost, minimizer
            # print "IS FINAL DEPTH"
            bestAction = ''
            lowestEvalNum = float("inf")
            #evalNum = -999999
            
            for action in game_state.getLegalActions(agentIndex):
              # print "lowest level", action
              newState = game_state.generateSuccessor(agentIndex, action)
              

              evalNum = self.evaluationFunction(newState)
              # print evalNum
              if evalNum < lowestEvalNum:
                lowestEvalNum = evalNum
                bestAction = action
              # if evalNum > bestMax:
              #   bestMax = evalNum
              # if evalNum < bestMin:
              #   bestMin = evalNum

              if lowestEvalNum < bestMax: return (lowestEvalNum, bestAction)
              bestMin = min(bestMin, lowestEvalNum)
            #pdb.set_trace()
            #print "@@@1: level: ", level, ";  agentIndex: ", agentIndex, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@2: best eval, action: ", lowestEvalNum, bestAction
            # print "lowest eval at last level", lowestEvalNum
            return (lowestEvalNum, bestAction)
          
          elif level % gameState.getNumAgents() == 0: #Pacman's turn, maximizer
            bestAction = 'Stop'
            highestEvalNum = float("-inf")
            #evalNum = -999999
            
            for action in game_state.getLegalActions(agentIndex):
              # print action
              newState = game_state.generateSuccessor(agentIndex, action)
              
              if newState.isWin():
                # print "IS WIN"
                evalNum = self.evaluationFunction(newState)
                # print evalNum
              elif newState.isLose():
                # print "IS LOSE", action
                evalNum = self.evaluationFunction(newState)
                # print evalNum
              else:
                
                evalNum , _  = alphabeta(newState, level + 1, bestMin, bestMax)
                # print evalNum

              if evalNum > highestEvalNum:
                highestEvalNum = evalNum
                bestAction = action
              # print "bestmin", bestMin
              if highestEvalNum > bestMin: return (highestEvalNum, bestAction)
              bestMax = max(bestMax, highestEvalNum)
              # print "bestMax, highestEvalNum", bestMax, highestEvalNum
            #pdb.set_trace()
            #print "@@@ 3: level: ", level, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@ 4: highest eval, action: ", highestEvalNum, bestAction
            return (highestEvalNum, bestAction)

          else: #Ghosts' turn, minimizer
            bestAction = 'Stop'
            lowestEvalNum = float("inf")
            #evalNum = 999999
            
            for action in game_state.getLegalActions(agentIndex):
              newState = game_state.generateSuccessor(agentIndex, action)
              # print action
              # if newState.isWin() or newState.isLose():
              #   print "IS WINLOSE"
              #   evalNum = self.evaluationFunction(newState)
              if newState.isWin():
                # print "IS WIN"
                evalNum = self.evaluationFunction(newState)
                # print evalNum
              elif newState.isLose():
                # print "IS LOSE", action
                evalNum = self.evaluationFunction(newState)
                # print evalNum
              else:
                #pdb.set_trace()
                evalNum , _  = alphabeta(newState, level + 1, bestMin, bestMax)
                # print evalNum

              if evalNum < lowestEvalNum:
                lowestEvalNum = evalNum
                bestAction = action
              # print "bestmax", bestMax
              if lowestEvalNum < bestMax: return (lowestEvalNum, bestAction)
              bestMin = min(bestMin, lowestEvalNum)
              # print "bestMin, lowestEvalNum", bestMin, lowestEvalNum
            
            #pdb.set_trace()
            #print "@@@  5: level: ", level, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@  6: lowest eval, action: ", lowestEvalNum, bestAction
            return (lowestEvalNum, bestAction)


    

        evalNum , action = alphabeta(gameState, 0, float("inf"), float("-inf")) #initially starts the level at 0
        # print "evalnum is:", evalNum
        return action

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
        finalLevel = gameState.getNumAgents() * self.depth 

        def expectimax(game_state, level):
          # Returns a tuple: (bestEvalNum, action)
          # bestEvalNum is the evalNum at this level, with this game_state
          # action is the action to take right now to get that bestEvalNum

          agentIndex = level % gameState.getNumAgents()

          if level >= finalLevel:
            print "Error with minimax function: levels_left should not be <= 0."
            return None
          
          elif level == finalLevel - 1: # must be a ghost, random action chooser!
            #bestAction = 'Stop'
            #lowestEvalNum = 999999
            #evalNum = -999999
            sumEvalNums = 0.0 # making it a float 
            actionsList = game_state.getLegalActions(agentIndex)

            for action in actionsList:
              newState = game_state.generateSuccessor(agentIndex, action)
              evalNum = self.evaluationFunction(newState)
              sumEvalNums += evalNum
            
            #pdb.set_trace()
            #print "@@@1: level: ", level, ";  agentIndex: ", agentIndex, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@2: best eval, action: ", lowestEvalNum, bestAction
            return (sumEvalNums / len(actionsList), '') # returning a blank action because the action doesn't matter
          
          elif level % gameState.getNumAgents() == 0: #Pacman's turn, maximizer
            bestAction = 'Stop'
            highestEvalNum = -999999
            #evalNum = -999999
            
            for action in game_state.getLegalActions(agentIndex):
              newState = game_state.generateSuccessor(agentIndex, action)
              
              if newState.isWin() or newState.isLose():
                evalNum = self.evaluationFunction(newState)
              else:
                #pdb.set_trace()
                evalNum , _ = expectimax(newState, level + 1)

              if evalNum > highestEvalNum:
                highestEvalNum = evalNum
                bestAction = action
            
            #pdb.set_trace()
            #print "@@@ 3: level: ", level, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@ 4: highest eval, action: ", highestEvalNum, bestAction
            return (highestEvalNum, bestAction)

          else: #Ghosts' turn, random action chooser!
            #bestAction = 'Stop'
            #lowestEvalNum = 999999
            #evalNum = 999999

            sumEvalNums = 0.0 # making it a float 
            actionsList = game_state.getLegalActions(agentIndex)

            for action in actionsList:
              newState = game_state.generateSuccessor(agentIndex, action)
              
              if newState.isWin() or newState.isLose():
                evalNum = self.evaluationFunction(newState)
              else:
                #pdb.set_trace()
                evalNum , _ = expectimax(newState, level + 1)

              sumEvalNums += evalNum
            
            #pdb.set_trace()
            #print "@@@1: level: ", level, ";  agentIndex: ", agentIndex, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@2: best eval, action: ", lowestEvalNum, bestAction
            return (sumEvalNums / len(actionsList), '') # returning a blank action because the action doesn't matter



            # for reference:
            for action in game_state.getLegalActions(agentIndex):
              newState = game_state.generateSuccessor(agentIndex, action)
              
              if newState.isWin() or newState.isLose():
                evalNum = self.evaluationFunction(newState)
              else:
                #pdb.set_trace()
                evalNum , _ = minimax(newState, level + 1)

              if evalNum < lowestEvalNum:
                lowestEvalNum = evalNum
                bestAction = action
            
            #pdb.set_trace()
            #print "@@@  5: level: ", level, ";  actions list: ", game_state.getLegalActions(agentIndex) 
            #print "@@@  6: lowest eval, action: ", lowestEvalNum, bestAction
            return (lowestEvalNum, bestAction)




        #pdb.set_trace()

        evalNum , action = expectimax(gameState, 0) #initially starts the level at 0
        #print "@@@0 evalnum is:", evalNum
        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    capsules = currentGameState.getCapsules() # capsules aka power pellets
    ghostStates = currentGameState.getGhostStates()
    numAgents = currentGameState.getNumAgents()
    minFoodDist = 1E9
    minCapsuleDist = 1E9
    minGhostDist = 1E9


    #for food
    for x in range(food.width):
      for y in range(food.height):
        if food[x][y]:
          foodManDist = abs(x - pos[0]) + abs(y - pos[1])
          
          if foodManDist < minFoodDist:
            minFoodDist = foodManDist
    if minFoodDist != 0:
      invMinFoodDist = 1.0 / minFoodDist
    else: 
      invMinFoodDist = 1.0 / 1

    # for capsules
    for capsulePos in capsules:
      capsuleManDist = abs(capsulePos[0] - pos[0]) + abs(capsulePos[1] - pos[1])
      if capsuleManDist < minCapsuleDist:
        minCapsuleDist = capsuleManDist
    if minCapsuleDist != 0:
      invMinCapsuleDist = 1.0 / minCapsuleDist
    else: 
      invMinCapsuleDist = 1.0 / 1

    #for ghosts
    for i in range(1, numAgents):
      ghostPos = currentGameState.getGhostPosition(i)
      ghostManDist = abs(ghostPos[0] - pos[0]) + abs(ghostPos[1] - pos[1])
      if ghostManDist < minGhostDist:
        minGhostDist = ghostManDist
    if minGhostDist !=0:
      invMinGhostDist = 1.0 / minGhostDist
    else:
      invMinGhostDist = 1.0 / 1
   

    if minGhostDist < 3:
      invMinGhostDist = invMinGhostDist * 100
    if minCapsuleDist < 3:
      invMinCapsuleDist = invMinCapsuleDist * 100

    

    totalScore = currentGameState.getScore() + invMinFoodDist - invMinGhostDist + invMinCapsuleDist - len(capsules)*1000
    
    return totalScore

# Abbreviation
better = betterEvaluationFunction

