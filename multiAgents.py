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
        currFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currPos = currentGameState.getPacmanPosition()
        score = successorGameState.getScore()   
		
        #How close is the food from the current state?
        food_positions_in_coordinates = util.matrixAsList(list(currFood))
        curr_food_distance = 0
        curr_food_score = 0
        for each_coordinate in food_positions_in_coordinates:
            curr_food_distance = util.manhattanDistance(each_coordinate,currPos)
            curr_food_score += float(1/float(curr_food_distance))
		
        
        #How close is the food from the next state?
        food_positions_in_coordinates = util.matrixAsList(list(newFood))
        next_food_distance = 0
        next_food_score = 0
        for each_coordinate in food_positions_in_coordinates:
            next_food_distance = util.manhattanDistance(each_coordinate,newPos)
            next_food_score += float(1/float(next_food_distance))
		
        
        #Check the difference in food scores
        if next_food_score > curr_food_score:
	        score += 3*(next_food_score - curr_food_score)
        else:
	        score += 3*(curr_food_score - next_food_score)

		    #Ghost distances from next position	
        next_ghost = 0		
        for each_ghost_instance in newGhostStates:	
            next_ghost = util.manhattanDistance(each_ghost_instance.getPosition(),newPos)
            if next_ghost < 2:
                score = score - 10   
 			
        return score 
		
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
		
        #Get number of agents from game state.		
        number_of_agents = gameState.getNumAgents()
		    #Get depth from self.
        depth = self.depth
		    #Go ntil max_game_depth.
        max_game_depth = depth * number_of_agents
        #Pacman successor action scores.
        successor_action_scores = []	

        def multi_mini_max(game_state, game_depth):
          # If the game_state is already in win position return score
          if game_state.isWin() or game_state.isLose():
              return game_state.getScore()
          # Check if max_depth defined for this game has been reached or not
          if game_depth >= max_game_depth:
              return game_state.getScore()
          
          #Classify as min or max (pacman or ghost)
          agent_index = game_depth % number_of_agents
          ''' Get the required legal actions for that index in game_state given to the function
              And removing STOP action from legal actions.  '''
          actions = game_state.getLegalActions(agent_index)
          if Directions.STOP in actions:
              actions.remove(Directions.STOP)
          
          #Pacman		  
          if agent_index == 0:
            maxim = float("-inf")
            for action in actions:
              nextgamestate = game_state.generateSuccessor(agent_index,action)
              ''' Sending the game_depth+1 to indicate go to the next agent in the depth defined '''
              val = multi_mini_max(nextgamestate, game_depth+1)
              maxim = max(maxim, val)
              ''' Storing the scores for the actions on level 1 to pick maximum.
                    (i.e., whether to got to E, W, N, S) '''
              if game_depth == 0:
                successor_action_scores.append(maxim)
            return maxim
		  
          #Ghost		  
          else: 
            minim = float("inf")
            for action in actions:
              nextgamestate = game_state.generateSuccessor(agent_index,action)
              ''' Sending the game_depth+1 to indicate go to the next agent in the depth defined. '''
              val = multi_mini_max(nextgamestate, game_depth+1)
              minim = min(minim, val)
            return minim

        # This function will select the action to be returned based on the scores from level 1.
        def max_pacman_action(gameState	):
          pacman_index = 0
          actions = gameState.getLegalActions(pacman_index)
          if Directions.STOP in actions:
              actions.remove(Directions.STOP)
          return actions[successor_action_scores.index(max(successor_action_scores))]
		
                  
        multi_mini_max(gameState, 0)
       
        return max_pacman_action(gameState)
		
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        #Get number of agents from game state.		
        number_of_agents = gameState.getNumAgents()
		    #Get depth from self.
        depth = self.depth
		    #Go until max_game_depth.
        max_game_depth = depth * number_of_agents
        #Pacman successor action scores.
        successor_action_scores = []	

        def alpha_beta_pruning(game_state, game_depth,alpha,beta):
          # If the game_state is already in win position return score
          if game_state.isWin() or game_state.isLose():
              return game_state.getScore()
          # Check if max_depth defined for this game has been reached or not
          if game_depth >= max_game_depth:
              return game_state.getScore()
          
          #Classify as min or max   (pacman or ghost)
          agent_index = game_depth % number_of_agents
          ''' Get the required legal actions for that index in game_state given to the function
              And removing STOP action from legal actions.  '''
          actions = game_state.getLegalActions(agent_index)
          if Directions.STOP in actions:
              actions.remove(Directions.STOP)
          
          #Pacman	(AgentIndex = 0). This will be max state where alpha will get updated 
          if agent_index == 0:
            maxim = float("-inf")
            for action in actions:
                nextgamestate = game_state.generateSuccessor(agent_index,action)
                ''' Sending the game_depth+1 to indicate go to the next agent in the depth defined
                    Sending alpha beta downwards furure uses '''
                val = alpha_beta_pruning(nextgamestate, game_depth+1,alpha,beta)
                maxim = max(maxim,val)
                if maxim > beta:          # Since in the question suggested not prune on euqality
                    return maxim				

                alpha = max(alpha, maxim)
                ''' Storing the scores for the actions on level 1 to pick maximum.
                    (i.e., whether to got to E, W, N, S) '''
                if game_depth == 0:
                    successor_action_scores.append(alpha)
            return maxim
		  
          #Ghost (AgentIndex >= 1). This will be min state where beta will get updated  
          else: 
            minim = float("inf")
            for action in actions:
                nextgamestate = game_state.generateSuccessor(agent_index,action)
                ''' Sending the game_depth+1 to indicate go to the next agent in the depth defined
                    Sending alpha beta downwards furure uses '''
                val = alpha_beta_pruning(nextgamestate, game_depth+1,alpha,beta)
                minim = min(minim,val)
                if minim < alpha:         # Since in the question suggested not prune on euqality
                    return minim				
                beta = min(beta, minim)
            return minim

        # This function will select the action to be returned based on the scores from level 1.
        def max_pacman_action(gameState):
          pacman_index = 0
          actions = gameState.getLegalActions(pacman_index)
          if Directions.STOP in actions:
              actions.remove(Directions.STOP)			  
          return actions[successor_action_scores.index(max(successor_action_scores))]

        alpha_beta_pruning(gameState, 0, float("-inf"), float("inf"))
        return max_pacman_action(gameState)

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
        #Get number of agents from game state.		
        number_of_agents = gameState.getNumAgents()
		    #Get depth from self.
        depth = self.depth
		    #Go until max_game_depth.
        max_game_depth = depth * number_of_agents
        #Pacman successor action scores.
        successor_action_scores = []	

        def expecti_max(game_state, game_depth):
          # If the game_state is already in win position return score
          if game_state.isWin() or game_state.isLose():
              return game_state.getScore()
          # Check if max_depth defined for this game has been reached or not
          if game_depth >= max_game_depth:
              return game_state.getScore()

          #Classify as min or max (pacman or ghost)
          agent_index = game_depth % number_of_agents
          ''' Get the required legal actions for that index in game_state given to the function
              And removing STOP action from legal actions.  '''
          actions = game_state.getLegalActions(agent_index)
          if Directions.STOP in actions:
              actions.remove(Directions.STOP)
          
          #Pacman		(AgentIndex = 0).
          if agent_index == 0:
            maxim = float("-inf")
            for action in actions:
              nextgamestate = game_state.generateSuccessor(agent_index,action)
              ''' Sending the game_depth+1 to indicate go to the next agent in the depth defined '''
              val = expecti_max(nextgamestate, game_depth+1)
              maxim = max(maxim, val)
              if game_depth == 0:
                successor_action_scores.append(maxim)
            return maxim
		  
          #Ghost (AgentIndex >= 1). This will be Expecti state where expectation will get calculated.
          else: 
            val = []
            for action in actions:
              nextgamestate = game_state.generateSuccessor(agent_index,action)
              ''' Sending the game_depth+1 to indicate go to the next agent in the depth defined '''
              val.append(float(expecti_max(nextgamestate, game_depth+1)))
            return (float(sum(val) / len(val)))

        # This function will select the action to be returned based on the scores from level 1.
        def max_pacman_action(gameState	):
          pacman_index = 0
          actions = gameState.getLegalActions(pacman_index)
          if Directions.STOP in actions:
              actions.remove(Directions.STOP)
          return actions[successor_action_scores.index(max(successor_action_scores))]
		    
        # Calling expectimax recursive function with start gamedepth as 0 such that it will be max (pacman).
        expecti_max(gameState, 0)
        return max_pacman_action(gameState)

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

