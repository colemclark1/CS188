# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    explored_set = set()
    frontier = []
    frontier_set = set()
    frontier.append([(problem.getStartState(), None)])
    while frontier:
        path = frontier.pop(0)
        current_state = path[-1][0]
        if current_state not in explored_set:
            # print explored_set
            explored_set.add(current_state)
            # print path
            triples = problem.getSuccessors(current_state)
            for triple in triples:
                if not (triple[0] in frontier_set or triple[0] in explored_set):
                    newpath = path[:]
                    # print path
                    successor = triple[0]
                    frontier_set.add(successor)
                    action = triple[1]
                    newpath.append((successor,action))
                    if (problem.isGoalState(successor)):
                        result = [x[1] for x in newpath]
                        return result[1:]
                    frontier.append(newpath)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    depth = 1
    while depth < 100000:
        optimalPath = DLS(problem, depth)
        if optimalPath:
            result = [x[1] for x in optimalPath]
            return result[1:]
        depth += 1
        # print depth

def DLS(problem, depth):
    explored_set = set()
    frontier = []
    frontier_set = set()
    frontier.append([(problem.getStartState(), None)])
    while frontier:
        path = frontier.pop(0)
        current_state = path[-1][0]
        if current_state not in explored_set and len(path) <= depth:
            # print explored_set
            explored_set.add(current_state)
            # print path
            triples = problem.getSuccessors(current_state)
            for triple in triples:
                if not (triple[0] in frontier_set or triple[0] in explored_set):
                    newpath = path[:]
                    # print path
                    successor = triple[0]
                    frontier_set.add(successor)
                    action = triple[1]
                    newpath.append((successor,action))
                    if (problem.isGoalState(successor)):
                        return newpath
                        # print frontier
                    frontier.insert(0,newpath)
    return None

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    explored_set = set()
    frontier = []
    frontier.append([(problem.getStartState(), None, 0)])
    while frontier:
        frontier = sorted(frontier, key=lambda x: x[-1][2])
        path = frontier.pop(0)
        current_triple = path[-1]
        current_state = current_triple[0]
        if problem.isGoalState(current_state):
            return [x[1] for x in path][1:]
        if (current_state in explored_set):
            continue
        explored_set.add(current_state)
        triples = problem.getSuccessors(current_state)
        for triple in triples:
            successor = triple[0]
            action = triple[1]
            stepCost = triple[2]
            if successor in explored_set:
                continue
            totalCost = problem.getCostOfActions([x[1] for x in path][1:]) + stepCost
            h = totalCost + heuristic(successor, problem)
            newPath = path[:]
            newPath.append((successor, action, h))
            frontier.append(newPath)
            # print frontier
            frontier = sorted(frontier, key=lambda x: x[-1][2])
    return None

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
