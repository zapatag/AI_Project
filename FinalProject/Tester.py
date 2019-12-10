from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint


def createTeam(firstIndex, secondIndex, isRed, first = 'OurReflexAgent', second = 'OurReflexAgent'):
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

class OurReflexAgent(CaptureAgent):

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)
    self.startingFood = 3
    print("Starting food is ", self.startingFood)

  def chooseAction(self, gameState):
    #Get every possible action from the current gameState
    actions = gameState.getLegalActions(self.index)
    myAgent = gameState.getAgentState(self.index)

    if myAgent.isPacman == False:
    	self.startingFood = 3

    #Retreat
    if self.startingFood == 0:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    #Gets the possible values returned from doing these actions
    values = [self.evaluate(gameState, a) for a in actions]

    #The highest of these possible values
    maxValue = max(values)

    if maxValue == 9999:
    	self.startingFood -= 1
    #The best of the possible actions to take based on maxValue
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)

    if (features['distanceToFood'] == 0):
    	return 9999

    return features * weights

  def ghostDistance(self, gameState):
    enemyDists = []
    oppPos = []
    myPos = gameState.getAgentPosition(self.index)
    opponentsIndex = self.getOpponents(gameState)
    oppPos.append(gameState.getAgentPosition(x) for x in opponentsIndex)
    oppDist = min([self.getMazeDistance(myPos, x) for x in oppPos])
    return oppDist

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()    
    features['successorScore'] = -len(foodList)

    if len(foodList) > 0:
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}