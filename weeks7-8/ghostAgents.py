# ghostAgents.py
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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util


class GhostAgent( Agent ):
    def __init__( self, index):
        self.index = index
    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist
class MinimaxGhost(GhostAgent):

    """
      Your minimax agent (question 1)

      useage: python2 pacman.py -p ExpectimaxAgent -l smallClassic -g MinimaxGhost -a depth=4
              python2 pacman.py -l smallClassic -g MinimaxGhost

    """
    "*** YOUR CODE HERE ***"
    def __init__(self, index, depth = '2'):
        self.index = index # Ghosts are always agent index > 0
        self.depth = int(depth)
    def getAction(self, gameState):
        start=1
        beg_agent=self.index 
        move=self.MinimaxEvaluationFunction(gameState,start,beg_agent)
        return move
    def MinimaxEvaluationFunction(self,gameState,depth,index):
        if (gameState.isLose())|(gameState.isWin()):
            return self.betterEvaluationFunctionGhost(gameState)
        if depth>self.depth:
            return self.betterEvaluationFunctionGhost(gameState)
        actions=[]
        for x in gameState.getLegalActions(index):
            actions.append(x)

        if index==0:
            goal=[]
            for x in actions:
                goal.append(self.MinimaxEvaluationFunction(gameState.generateSuccessor(index,x),depth+1,self.index))
            if index!=self.index:
                return max(goal)
            elif (depth!=1)&(index==self.index): 
                return min(goal)
            else: 
                choices=[]
                for index in range(len(goal)):
                    if goal[index]==min(goal):
                        choices.append(index)
                One=random.choice(choices)
                return actions[One]
        else:
            goal=[]
            for x in actions:
                goal.append(self.MinimaxEvaluationFunction(gameState.generateSuccessor(index,x),depth,0))
            if index!=self.index: 
                return max(goal)
            elif (depth!=1)&(index==self.index): 
                return min(goal)
            else: 
                choices=[]
                for index in range(len(goal)):
                    if goal[index]==min(goal):
                        choices.append(index)
                One=random.choice(choices)
                return actions[One]
    def betterEvaluationFunctionGhost(self,currentGameState):
        pcPos=currentGameState.getPacmanPosition()
        ghPos=currentGameState.getGhostPosition(self.index)
        return manhattanDistance(pcPos,ghPos)

# Abbreviation
def scoreEvaluationFunctionGhost(currentGameState):
    """
        Ghost evaluation function
    """
    return currentGameState.getScore()
def betterEvaluationFunctionGhost(currentGameState):
    """
        Ghost evaluation function
    """
    return currentGameState.getScore()


# Abbreviation
ghostEval = betterEvaluationFunctionGhost

