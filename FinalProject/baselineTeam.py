# baselineTeam.py
# ---------------
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


# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
 
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    self.foodCount = 0
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(self.getFood(gameState).asList())
    '''
    enemyDists = []
    myPos = gameState.getAgentPosition(self.index)
    if self.red:
      opponentsIndexRed = self.getOpponents(gameState)
      enemyDists.append(gameState.getAgentPosition(x) for x in opponentsIndexRed)
      opp1 = opponentsIndexRed[0]
      oppPos = gameState.getAgentPosition(opp1)
      print("MY POSITION", myPos)
      print("opp index: ", opponentsIndexRed)
      print("Opponent: ", opp1, " position: ", oppPos)
      print("Dist to enemy: ", opponentsIndexRed[0], " from friendly pacman: ", self.index)
      print("The distance is: ", self.getMazeDistance(myPos, oppPos))
    if self.red:
      print(myPos)
    '''
    #if self.red:
    #print(enemyDists[x] for x in enemyDists)
    #enemyDist = (self.getMazeDistance(myPos, x[][1:2]) for x in opponents)
    
    me = gameState.getAgentState(self.index)
    if foodLeft <= 2 or self.foodCount > 1: #or (x in enemyDists < 8):
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      if me.isPacman == False:
        self.foodCount = 0
        pass
      return bestAction
    #else:
    #finalAction = random.choice(bestActions)
    finalAction = min(bestActions)
    me = gameState.getAgentState(self.index)
    #finalAction = random.choice(bestActions)
    successor = self.getSuccessor(gameState, finalAction)
    lastFood = self.getFood(gameState).asList()
    #print("LAST FOOD: ", lastFood)
    nextFood = self.getFood(successor).asList()
    #print("NEXT FOOD: ", nextFood)
    #print(gameState.getNumAgents())

    if (lastFood == nextFood) == False:
      self.foodCount += 1
    if me.isPacman == False:
      self.foodCount = 0

    #print("FOOD COUNT BOI!! ", self.foodCount, " FOR THE HOMIE: ", self.index)

    return finalAction

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    '''
    #print("OFFENSIVE FOODLIST: ", foodList)
    me = gameState.getAgentState(self.index)
    #successor = self.getSuccessor(gameState, action)
    lastFood = self.getFood(gameState).asList()
    #print("LAST FOOD: ", lastFood)
    nextFood = self.getFood(successor).asList()
    #print("NEXT FOOD: ", nextFood)

    if (lastFood == nextFood) == False:
      #if gameState.getAgentPosition(self.index) in foodList:
      self.foodCount += 1
    if me.isPacman == False:
      self.foodCount = 0
    '''
    features['successorScore'] = -len(foodList)#self.getScore(successor)

    # Compute distance to the nearest food

    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}

  def ghostDistance(self, gameState):
    #this field is for holding the opponents positions in a list
    #e.g. [(2, 6), (18, 9)]
    oppPos = []
    #the position of the current agent e.g. (12, 2)
    myPos = gameState.getAgentPosition(self.index)

    #gets the indices of our opponents (relevant since our code can
    # end up on either blue or red side)
    opponentsIndex = self.getOpponents(gameState)
    #append position of all opponents to list oppPos
    oppPos.append(gameState.getAgentPosition(x) for x in opponentsIndex)
    #calculates the distance of the closest enemy
    oppDist = min([self.getMazeDistance(myPos, x) for x in oppPos])
    return oppDist
    '''
    if self.red:
      opponentsIndexRed = self.getOpponents(gameState)
      enemyDists.append(gameState.getAgentPosition(x) for x in opponentsIndexRed)
      opp1 = opponentsIndexRed[0]
      #oppPos = gameState.getAgentPosition(opp1)
      print("MY POSITION", myPos)
      print("opp index: ", opponentsIndexRed)
      print("Opponent: ", opp1, " position: ", oppPos)
      print("Dist to enemy: ", opponentsIndexRed[0], " from friendly pacman: ", self.index)
      print("The distance is: ", self.getMazeDistance(myPos, oppPos))
    '''