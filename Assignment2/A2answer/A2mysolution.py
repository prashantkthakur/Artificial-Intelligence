def iterativeDeepeningSearch(startState, goalState,
                             actionsF, takeActionF, maxDepth):
    for depth in range(maxDepth):
        result = depthLimitedSearch(startState, goalState,
                                    actionsF, takeActionF, depth)
        if result is 'failure':
            return 'failure'
        if result is not 'cutoff':
            result.insert(0, startState)
            return result
    return 'cutoff'


def depthLimitedSearch(state, goalState,
                       actionsF, takeActionF, depthLimit):
    if state == goalState:
        return []
    if depthLimit == 0:
        return 'cutoff'
    cutoffOccurred = False
    for action in actionsF(state):
        childState = takeActionF(state, action)
        result = depthLimitedSearch(childState, goalState,
                                    actionsF, takeActionF, depthLimit-1)
        if result is 'cutoff':
            cutoffOccurred = True
        elif result is not 'failure':
            result.insert(0, childState)
            return result
    if cutoffOccurred:
        return 'cutoff'
    else:
        return 'failure'

######################################################################
# Eight Puzzle


def findBlank_8p(s):
    return iTorc(s.index(0))


def actionsF_8p(state):
    r, c = findBlank_8p(state)
    actions = []
    if c > 0:
        actions.append('left')
    if c < 2:
        actions.append('right')
    if r > 0:
        actions.append('up')
    if r < 2:
        actions.append('down')
    return actions


def takeActionF_8p(state, action):
    import copy
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
    return state


def goalTestF_8p(s, goalState):
    return s == goalState


def printPath_8p(start, goal, solutionPath):
    print('\n\nPath from')
    printState_8p(start)
    print('  to')
    printState_8p(goal)
    if solutionPath is 'cutoff':
        print('was not found due to depth cutoff.')
    elif solutionPath is 'failure':
        print('cannot be found.')
    else:
        print('  is', len(solutionPath), 'nodes long:')
        indent = 0
        for s in solutionPath:
            printState_8p(s, indent)
            print()
            indent += 1


def printState_8p(state, indent=0):
    st = list(map(str, state))
    st[st.index('0')] = '-'
    blanks = ' '*indent
    for i in range(0, 9, 3):
        print('{} {} {} {}'.format(blanks, st[0+i], st[1+i], st[2+i]))


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



if __name__ == '__main__':

    startState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    goalState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    path = iterativeDeepeningSearch(startState, goalState,
                                    actionsF_8p, takeActionF_8p, 5)
    printPath_8p(startState, goalState, path)

    startState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    goalState = [0, 1, 1, 1, 1, 1, 1, 1, 1]
    path = iterativeDeepeningSearch(startState, goalState,
                                    actionsF_8p, takeActionF_8p, 5)
    printPath_8p(startState, goalState, path)
    print('Depth limit was 5')

    startState = [1, 5, 0, 4, 7, 2, 6, 8, 3]
    goalState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    path = iterativeDeepeningSearch(startState, goalState,
                                    actionsF_8p, takeActionF_8p, 5)
    printPath_8p(startState, goalState, path)
    print('Depth limit was 5')

    startState = [1, 5, 0, 4, 7, 2, 6, 8, 3]
    goalState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    path = iterativeDeepeningSearch(startState, goalState,
                                    actionsF_8p, takeActionF_8p, 10)
    printPath_8p(startState, goalState, path)
    print('Depth limit was 10')
