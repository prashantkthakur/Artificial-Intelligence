import numpy as np
import random
import copy

#Check the search graph
def aF(state):
    return copy.copy(succs.get(state,[]))
def tAF(state, action):
    return action

# End of search tree implementation


def iterativeDeepeningSearch(startState, goalState, actionsF, takeActionF, maxDepth):
    for depth in range(maxDepth):
        # print("IT depth {}".format(depth))
        result = depthLimitedSearch(startState, goalState, actionsF, takeActionF, depth)
        # print("IT Result found!!!!! result={}, startstate={} depth={}".format(result, startState, depth))
        if result is 'failure':
            return 'failure'
        if result is not 'cutoff':
            # print("ITerative result={}".format(result))
            #Add startState to front of solution path, in result, returned by depthLimitedSearch
            result.insert(0,startState) ## --changex
            return result
    return 'cutoff'


def depthLimitedSearch(state, goalState, actionsF, takeActionF, depthLimit):
    # print(".........State at beginning: start={} depth={}".format(state,depthLimit))
    if state == goalState:
        #solutionPath.append(state)
        # print("state = goal solutionpath={}".format(state))
        # return [state]
        return []#-- changex

    if depthLimit is 0:
        # signal that the depth limit was reached
        # print("Depth 0 so returning cutoff")
        return 'cutoff'
    cutoffOccurred = False
    for action in actionsF(state):
        childState = takeActionF(state, action)
        # print("action and childstate= action={} childstate={} startState={}".format(action,childState,state))
        result = depthLimitedSearch(childState, goalState, actionsF, takeActionF, depthLimit-1)
        # print("Result found!!!!! result={}, startstate={}".format(result, state))
        if result is 'cutoff':
            cutoffOccurred = True
        elif result is not 'failure':
            #Add childState to front of partial solution path, in result, returned by depthLimitedSearch
            # print("Result found!!!!! result={}, state={} depth={},action={}".format(result,state,depthLimit,action))
            # result.insert(0,state)
            result.insert(0,childState) #--changex
            # print("Solution path if result success. {}".format(result))
            return result
    if cutoffOccurred:
        return 'cutoff'
    else:
        return 'failure'


def generateNpArray(state,list=False):
    if list:
        return state.reshape(1, 9)[0].tolist()
    else:
        return np.array(state).reshape(3, 3)


def printState_8p(state):
    np_array = generateNpArray(state)
    print('\n'.join(str(a).strip('[]').replace('0', ' ') for a in np_array))


def findBlank_8p(state):
    np_array = generateNpArray(state)
    idx = np.argwhere(np_array == 0)
    return tuple(idx[0])


def actionsF_8p(state):
    position = findBlank_8p(state)
    action = ['left', 'right', 'up', 'down']
    if position[0] == 0:
        action.remove('up')
    if position[0] == 2:
        action.remove('down')
    if position[1] == 0:
        action.remove('left')
    if position[1] == 2:
        action.remove('right')
    return action


def takeActionF_8p(state, action):
    np_array = generateNpArray(state)
    position = findBlank_8p(state)
    try:
        if action == 'left':
            np_array[position], np_array[(position[0], position[1]-1)] = np_array[(position[0],position[1]-1)], np_array[position]
        if action == 'right':
            np_array[position], np_array[(position[0], position[1]+1)] = np_array[(position[0],position[1]+1)], np_array[position]
        # swap the value with the top row whose row is 1 unit less.
        if action == 'up':
            np_array[position], np_array[(position[0]-1, position[1])] = np_array[(position[0]-1,position[1])], np_array[position]

        if action == 'down':
            np_array[position], np_array[(position[0]+1, position[1])] = np_array[(position[0]+1,position[1])], np_array[position]
    except IndexError:
        print("Wrong Action applied.\n Action ={} on .. \n{}".format(action,printState_8p(state)))
    return generateNpArray(np_array,list=True)


def printPath_8p(startState, goalState, path):
    print("Path from\n{} \n to {} \n is {} nodes long.\n".format(startState,goalState,len(path)))
    for item in path:
        print("\n")
        printState_8p(item)


def action_waterjug(state):
    result = set()
    x,y = state[0],state[1]
    if x < 4:
        result.add((4, y))
    if y < 3:
        result.add((x, 3))
    if x > 0:
        result.add((0, y))
    if y > 0:
        result.add((x, 0))
    if y > 0 and ((x+y <= 4) and (x+y > 0)):
        if y-(4-x) >=0:
            result.add((4, y-(4-x)))
    if x > 0 and ((x+y >= 3) and (x+y > 0)):
        result.add((x-(3-y), 3))
    if (x+y) <= 4 and y > 0:
        val = ((x+y),0)
        result.add(val)
    if (x+y) <= 3 and x > 0:
        val =(0,x+y)
        result.add(val)
    return list(result)

def takeAction_waterjug(state,action):
    return action


st = [1, 0, 3, 4, 2, 5, 6, 7, 8]
# print(printState_8p(st))
goal = [1, 2, 3, 4, 0, 5, 6, 7, 8]#[1, 2, 3, 4, 0, 5,6, 7, 8]
sln = depthLimitedSearch(st,goal,actionsF_8p,takeActionF_8p,3)
# Returns different path than above as the left most deepest solution is found instead of optimal one.
sln1 = depthLimitedSearch(st,goal,actionsF_8p,takeActionF_8p,5)
# No matter what is the depth, it always finds the best solution as it checks all the nodes at one level
# and see if there is any solution
sol = iterativeDeepeningSearch(st,goal, actionsF_8p,takeActionF_8p,3)
print(sln)
print(sln1)
print(sol)

def randomStartState(goalState, actionsF, takeActionF, nSteps):
    state = goalState
    for i in range(nSteps):
        state = takeActionF(state, random.choice(actionsF(state)))
        print(state)
    return state
graph={'e': ['z'], 'a': ['b', 'z', 'd'], 'b': ['a'], 'y': ['z'], 'd': ['y']}
# a=randomStartState(st, actionsF_8p,takeActionF_8p,10)
# print(a)

succs = {'a': ['b', 'z', 'd'], 'b':['a'], 'e':['z'], 'd':['y'], 'y':['z']}
# path1 = iterativeDeepeningSearch('a', 'y', aF, tAF, 1)
path2 = iterativeDeepeningSearch('a', 'y', aF, tAF, 5)
print("path2={}".format(path2))