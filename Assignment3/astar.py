# Recursive Best First Search (Figure 3.26, Russell and Norvig)
#  Recursive Iterative Deepening form of A*, where depth is replaced by f(n)
from math import sqrt, ceil
class Node:
    def __init__(self, state, f=0, g=0,h=0):
        self.state = state
        self.f = f
        self.g = g
        self.h = h
    def __repr__(self):
        return "Node(" + repr(self.state) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"


#############################################################################################
# IDS and DS
def iterativeDeepeningSearch(startState, goalState,actionsF, takeActionF, maxDepth):
    global nNode
    nNode = [0,0] # [depth,nodes]
    for depth in range(maxDepth):
        result = depthLimitedSearch(startState, goalState,actionsF, takeActionF, depth)
        if result is 'failure':
            return 'failure'
        if result is not 'cutoff':
            result.insert(0, startState)
            return (result,nNode)
    return 'cutoff'


def depthLimitedSearch(state, goalState,actionsF, takeActionF, depthLimit):
    # global nNode
    if state == goalState:
        return []
    if depthLimit == 0:
        return 'cutoff'
    cutoffOccurred = False
    for action in actionsF(state):
        nNode[1] +=1
        childState,_= takeActionF(state, action)
        result = depthLimitedSearch(childState, goalState,actionsF, takeActionF, depthLimit-1)
        if result is 'cutoff':
            cutoffOccurred = True
        elif result is not 'failure':
            nNode[0]+=1
            result.insert(0, childState)
            return result
    if cutoffOccurred:
        return 'cutoff'
    else:
        return 'failure'


# End of IDS and DS
#####################################################################################
# A-start start
def aStarSearch(startState, actionsF, takeActionF, goalTestF, hF):
    global aNode
    aNode = [0,0] # [depth,nodes]
    h = hF(startState)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    return aStarSearchHelper(startNode, actionsF, takeActionF, goalTestF, hF, float('inf'))


def aStarSearchHelper(parentNode, actionsF, takeActionF, goalTestF, hF, fmax):
    if goalTestF(parentNode.state):
        return ([parentNode.state], parentNode.g)
    ## Construct list of children nodes with f, g, and h values
    actions = actionsF(parentNode.state)
    if not actions:
        return ("failure", float('inf'))
    children = []
    for action in actions:
        # print(aNode, ":",action, parentNode.state)
        aNode[1] += 1
        (childState,stepCost) = takeActionF(parentNode.state, action)
        # print(childState)
        h = hF(childState)
        g = parentNode.g + stepCost
        f = max(h+g, parentNode.f)
        childNode = Node(state=childState, f=f, g=g, h=h)
        children.append(childNode)
    while True:
        # find best child
        children.sort(key = lambda n: n.f) # sort by f value
        bestChild = children[0]
        if bestChild.f > fmax or bestChild.f == float('inf'):
            return ("failure",bestChild.f)
        # next lowest f value
        alternativef = children[1].f if len(children) > 1 else float('inf')
        # expand best child, reassign its f value to be returned value
        result,bestChild.f = aStarSearchHelper(bestChild, actionsF, takeActionF, goalTestF,
                                            hF, min(fmax,alternativef))
        if result is not "failure":
            # Gives depth of search
            aNode[0] += 1
            result.insert(0,parentNode.state)
            return (result, bestChild.f)

# A-start End

######################################################################
# Eight Puzzle


def findBlank_8p(s):
    return iTorc(s.index(0))


def actionsF_8p(state):
    r, c = findBlank_8p(state)
    actions = []
    if c > 0:
        actions.append(('left',1))
    if c < 2:
        actions.append(('right',1))
    if r > 0:
        actions.append(('up',1))
    if r < 2:
        actions.append(('down',1))
    return actions


def takeActionF_8p(state, action):
    import copy
    # action passed has (actual_action, cost)
    action,cost = action
    state = copy.deepcopy(state)
    r, c = findBlank_8p(state)
    dr = dc = 0
    if action is 'left':
        dc -= 1
    elif action is 'right':
        dc += 1
    elif action is 'up':
        dr -= 1
    elif action is 'down':
        dr += 1
    newr, newc = r+dr, c+dc
    setTile(state, r, c, getTile(state, newr, newc))
    setTile(state, newr, newc, 0)
    return (state,cost)


def goalTestF_8p(s, goalState):
    return s == goalState

def rcToi(row, col):
    return row*3+col


def iTorc(i):
    row = i // 3
    col = i - row*3
    return (row, col)

def setTile(state, row, col, tile):
    state[rcToi(row, col)] = tile
    return state

def getTile(state, row, col):
    return state[rcToi(row, col)]
# End of 8-puzzle
##########################################################################
# Heuristic functions start
def h1_8p(state,goal):
    return 0

#Manhattan distance of blank space
def h2_8p(state,goal):
    sc = findBlank_8p(state)
    gc = findBlank_8p(goal)
    dist = abs(gc[0]-sc[0])+abs(gc[1]-sc[1])
    return dist

#Eculadian distance of blank space
def h2a_8p(state,goal):
    sx,sy = findBlank_8p(state)
    gx,gy = findBlank_8p(goal)
    return ceil(sqrt((gx-sx)**2+(gy-sy)**2))


# Manhattan distance- sum of all misplaced values
def h3_8p(state,goal):
    sum = 0
    for item in state:
        sc = iTorc(state.index(item))
        gc = iTorc(goal.index(item))
        if sc != gc and item !=0:
            sum += abs(sc[0]-gc[0])+abs(sc[1]-gc[1])
    return sum

def h4_8p(state,goal):
    val=0
    for item in state:
        sc = iTorc(state.index(item))
        gc = iTorc(goal.index(item))
        if sc != gc:
            val +=1
    return val

def h5_8p(state,goal):
    return max(h3_8p(state,goal),h4_8p(state,goal))

# End of Heuristic functions
###########################################################################
# Start EBF
def eqn_sum(c,d):
    sum = 1
    while d != 0:
        sum += c**(d)
        d = d-1
    return sum
    # if b==1:
    #     return (1-b**(d+1))/0.0001
    # else:
    #     return (1-b**(d+1))/(1-b)
def ebf1(nNodes, depth, precision=0.01):
    func = lambda b: (1 - b**(depth+1))/0.00001 if b==1 else (1 - b**(depth+1)) / (1-b)
    bLow = 0.0
    bHigh = nNodes
    counter = 0
    calcNodes = func(bLow)
    while abs(calcNodes-nNodes) > precision and counter < 10000:
        midpoint = (bLow+bHigh)/2
        calcNodes = func(midpoint)
        if calcNodes-nNodes < 0:
            bLow = midpoint
        else:
            bHigh = midpoint
        counter += 1
    return bHigh

def ebf(N,d,precision=0.01):
    if N <=0:
        return 0.0
    low = 0.0
    high = N
    limit =0
    mid = float(high)
    while abs(eqn_sum(mid,d)-N) > precision and limit < 50000:
        # print(eqn_sum(mid,d)-N, precision)
        mid = (low+high)/2.0
        if eqn_sum(mid,d) > N:
            high = mid
        else:
            low = mid
        limit += 1
    return mid

def runExperiment(goalState1, goalState2, goalState3,h):
    state = [1,2,3,4,0,5,6,7,8]
    # MAX DEPTH OF IDS
    max_depth = 15
    print('\t\t\t{}\t\t\t{}\t\t\t{}'.format(goalState1,goalState2,goalState3))
    print('{}{:>10}{:>8}{:>10}{:>18}{:>10}{:>8}{:>15}{:>8}{:>12}'.format('Algorithm','Depth','Nodes','EBF','Depth','Nodes','EBF','Depth','Nodes','EBF'))
    # print("{}\t\t{}\t{}\t{}\t\t{}\t{}\t{}\t\t{}\t{}\t{}".format())
    value_ids=["IDS"]
    value_as ={'h1_8p':["A*h1"], 'h2_8p':["A*h2"],'h3_8p':["A*h3"]}
    for i in [goalState1,goalState2,goalState3]:
        iterativeDeepeningSearch(state, i, actionsF_8p, takeActionF_8p, maxDepth=max_depth)
        value_ids.extend(nNode)
        value_ids.append(ebf(nNode[1],nNode[0]))
        for hf in h:
            aStarSearch(state, actionsF_8p, takeActionF_8p, lambda s: goalTestF_8p(s, i),lambda s: hf(s, i))
            value_as[hf.__name__].extend(aNode)
            value_as[hf.__name__].append(ebf(aNode[1],aNode[0]))
        # print (value_as)
    print('{}\t\t\t\t{}\t\t{}\t\t{:.3f}\t\t\t\t{:<}\t\t{:<}\t\t{:.3f}\t\t\t{}\t\t{:<}\t\t{:.3f}'.format(value_ids[0],value_ids[1],value_ids[2],value_ids[3],value_ids[4],value_ids[5],value_ids[6],value_ids[7],value_ids[8],value_ids[9]))
    print('{}\t\t\t{}\t\t{}\t\t{:.3f}\t\t\t\t{}\t\t{}\t\t{:.3f}\t\t\t{}\t\t{:<}\t\t{:.3f}'.format(value_as['h1_8p'][0],value_as['h1_8p'][1],value_as['h1_8p'][2],value_as['h1_8p'][3],value_as['h1_8p'][4],value_as['h1_8p'][5],value_as['h1_8p'][6],value_as['h1_8p'][7],value_as['h1_8p'][8],value_as['h1_8p'][9]))
    print('{}\t\t\t{}\t\t{}\t\t{:.3f}\t\t\t\t{}\t\t{}\t\t{:.3f}\t\t\t{}\t\t{:<}\t\t{:.3f}'.format(value_as['h2_8p'][0],value_as['h2_8p'][1],value_as['h2_8p'][2],value_as['h2_8p'][3],value_as['h2_8p'][4],value_as['h2_8p'][5],value_as['h2_8p'][6],value_as['h2_8p'][7],value_as['h2_8p'][8],value_as['h2_8p'][9]))
    print('{}\t\t\t{}\t\t{}\t\t{:.3f}\t\t\t\t{}\t\t{}\t\t{:.3f}\t\t\t{}\t\t{:<}\t\t{:.3f}'.format(value_as['h3_8p'][0],value_as['h3_8p'][1],value_as['h3_8p'][2],value_as['h3_8p'][3],value_as['h3_8p'][4],value_as['h3_8p'][5],value_as['h3_8p'][6],value_as['h3_8p'][7],value_as['h3_8p'][8],value_as['h3_8p'][9]))

def runExperiment1(goalState1, goalState2, goalState3,h):
    state = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    def prepare_value(data):
        depth.append(data[0])
        nodes.append(data[1])
        ebff.append(ebf(data[1],data[0]))

    g1 = str(goalState1)
    g2 = str(goalState2)
    g3 = str(goalState3)

    header = pd.MultiIndex.from_product([[g1,g2,g3],['Depth','Nodes','EBF']],names=['','Algorithms'])
    df = pd.DataFrame(columns=header, index=["IDS","A*h1","A*h2","A*h3"])
    for i in [goalState1,goalState2,goalState3]:
        depth = []
        nodes = []
        ebff = []
        iterativeDeepeningSearch(state,i, actionsF_8p, takeActionF_8p, 13)
        prepare_value(nNode)
        for hf in h:
            aStarSearch(state,actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s,i),lambda s: hf(s,i))
            prepare_value(aNode)

        df[(str(i),'Depth')] = depth
        df[(str(i),"Nodes")] = nodes
        df[(str(i),"EBF")] = ebff
    print(df)
# End EBF
#######################################################
if __name__ == "__main__":

    '''
    successors = {'a': ['b','c'],
                  'b': ['d','e'],
                  'c': ['f'],
                  'd': ['g', 'h'],
                  'f': ['i','j']}

    def actionsF(s):
        try:
            ## step cost of each action is 1
            return [(succ,1) for succ in successors[s]]
        except KeyError:
            return []
    def takeActionF(s,a):
        return a
    def goalTestF(s):
        return s == goal
    def h1(s):
        return 0


    def actionsF_simple(state):
        succs = {'a': ['b', 'c'], 'b': ['a'], 'c': ['h'], 'h': ['i'], 'i': ['j', 'k', 'l'], 'k': ['z']}
        return [(s, 1) for s in succs.get(state, [])]


    def takeActionF_simple(state, action):
        return action


    def goalTestF_simple(state, goal):
        return state == goal


    def h_simple(state, goal):
        return 1
    '''
    start = 'a'
    goal = 'j'
    # result = aStarSearch(start,actionsF,takeActionF,goalTestF,h1)
    # print('Path from a to h is', result[0], 'for a cost of', result[1])
    # actions = actionsF_simple('a')
    # print (takeActionF_simple('a', actions[0]))
    # print(goalTestF_simple('a', 'a'))
    # print(h_simple('a', 'z'))
    state=[1, 2, 3, 4, 0, 5, 6, 7, 8]
    goal0= state
    goal1=[1, 2, 3, 4, 5, 8, 6, 0, 7]
    goal2 = [1, 0, 3, 4, 5, 8, 2, 6, 7]
    print(h3_8p(state,goal1))
    result=aStarSearch(state,actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s,goal1),lambda s: h3_8p(s,goal1))
    print(aNode)
    result2=aStarSearch(state,actionsF_8p, takeActionF_8p,lambda s: goalTestF_8p(s,goal2),lambda s: h5_8p(s,goal2))
    # print(result)
    print(result2)
    print("Astart: h4_8p:",aNode)
    print(ebf1(3,2))
    print(ebf(3,2))
    # print (iterativeDeepeningSearch([1,2,3,4,0,5,6,7,8],[1, 2, 3, 4, 5, 8, 6, 0, 7], actionsF_8p, takeActionF_8p, 4))
    # print(nNode)
    # runExperiment1(goal0,goal1,goal2,[h1_8p,h2_8p,h3_8p])
    # print(ebf(2,1))

    # # print(actionsF_8p([1,3,2,4,0,5,6,7,8]))
    # # print(takeActionF_8p([1,3,2,4,5,0,6,7,8],('left',1)))

    # print(h2_8p(goal,state))