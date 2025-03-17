# search.py
# ---------
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

import torch
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import heapq

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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #整体逻辑和bfs大致相同，不过使用stack后进先出的数据结构
    #值得注意：dfs和bfs在对已经访问的结点标记为visited的时候不一样
    Frontier = util.Stack()
    Visited = []
    Frontier.push( (problem.getStartState(), []) )

    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        #真实访问结点时才加入visited
        Visited.append( state ) 
        if problem.isGoalState(state):
            #print 'Find Goal'
            return actions 
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            if n_state not in Visited:
                #若该节点的直接子节点没有访问过压入栈中，且后进先出
                Frontier.push( (n_state, actions + [n_direction]) )
                #dfs与bfs不同，先压入栈中的结点后访问，不可以标记为visited让后压入的无法访问
                
    util.raiseNotDefined()

    
#! 例题答案如下
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs --frameTime 0
    #python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5 --frameTime 0
    "*** YOUR CODE HERE ***"

    Frontier = util.Queue()
    Visited = []
    Frontier.push( (problem.getStartState(), []) )
    #print 'Start',problem.getStartState()
    Visited.append( problem.getStartState() )

    while Frontier.isEmpty() == 0:
        state, actions = Frontier.pop()
        if problem.isGoalState(state):
            #print 'Find Goal'
            return actions 
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            if n_state not in Visited:
                #bfs先压入的标记为visited，后续若又压入肯定再更早的位置已经访问过
                Frontier.push( (n_state, actions + [n_direction]) )
                Visited.append( n_state )
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    Frontier = util.PriorityQueue() #维护一个待访问的堆
    #用于记录已经确定访问路线的节点
    Expanded = set()
    Frontier.push( problem.getStartState(),0 ) #仅记录结点和cost，actions序列另保存
    action_dic={problem.getStartState():[]} #用一个dictionary来记录当前到某个结点最短路径的action序列

    while Frontier.isEmpty() == 0:

        state = Frontier.pop() # 此时前面的action已经为确定
        actions=action_dic[state] #目前到state的最短路径
        cost = problem.getCostOfActions(actions)
        #if state not in Expanded:
        Expanded.add(state) #标记已访问过当前结点
        if problem.isGoalState(state): #当前结点为目标结点
            #print 'Find Goal'
            return action_dic[state] 
        
        #遍历当前结点的直接相邻节点，更新相邻节点的最短路径
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            n_cost=next[2]
            if n_state not in Expanded: #该节点还未访问过
                if n_state not in action_dic:
                    action_dic[n_state]= actions + [n_direction]
                    Frontier.push(n_state , cost+n_cost)
                elif n_state in action_dic and problem.getCostOfActions(action_dic[n_state]) > cost +n_cost :
                    action_dic[n_state]=actions + [n_direction]
                    Frontier.update(n_state , cost+n_cost)
                else:
                    continue #无需更新最短路径
                    
    util.raiseNotDefined()
# 一些思考
# 当我们的堆为Frontier.push( (状态，路径)，cost）的时候
#可能存在同一个状态以不同路径成本存在于队列中多次的情况。只有当该状态被弹出时，才确认这是到达该状态的最低成本路径，因此需要标记为已扩展，避免再次处理
# 此处frontier的update函数可自动替换的是cost，而第一项的元组，即使n_state一样，到那的路径可能不同


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #整体思路和USC类似，不过priorityqueue比较的priority加上一个启发函数
    #维护一个待访问的堆，堆元素（item，priority）
    #item为（state）,priority为hueristic+usc
    Frontier = util.PriorityQueue() #维护一个待访问的堆
    #用于记录已经确定访问路线的节点
    Expanded = set()
    Frontier.push( problem.getStartState(),heuristic(problem.getStartState(),problem) ) #仅记录结点和cost，actions序列另保存
    action_dic={problem.getStartState():[]} #用一个dictionary来记录当前到某个结点最短路径的action序列

    while Frontier.isEmpty() == 0:

        state = Frontier.pop() # 此时前面的action已经为确定
        actions=action_dic[state] #目前到state的最短路径
        cost = problem.getCostOfActions(actions)
        #if state not in Expanded:
        Expanded.add(state) #标记已访问过当前结点
        if problem.isGoalState(state): #当前结点为目标结点
            #print 'Find Goal'
            return action_dic[state] 
        
        #遍历当前结点的直接相邻节点，更新相邻节点的最短路径
        for next in problem.getSuccessors(state):
            n_state = next[0]
            n_direction = next[1]
            n_cost=next[2]
            n_heuristic=heuristic(n_state,problem)
            if n_state not in Expanded: #该节点还未访问过
                if n_state not in action_dic:
                    action_dic[n_state]= actions + [n_direction]
                    Frontier.push(n_state , cost+n_cost+n_heuristic)
                elif n_state in action_dic and problem.getCostOfActions(action_dic[n_state]) > cost +n_cost :
                    action_dic[n_state]=actions + [n_direction]
                    Frontier.update(n_state , cost+n_cost+n_heuristic)
                else:
                    continue #无需更新最短路径
                    
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
