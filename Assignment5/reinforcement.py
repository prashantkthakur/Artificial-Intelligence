import numpy as np
import copy
import random


def padding(state,pad):
    clone = copy.deepcopy(state)
    length = list(map(lambda x: len(x), state))
    # Pad blank at the beginning
    for val in clone:
        if len(val) < max(length):
            for i in range(max(length) - len(val)):
                val[:0] = pad
    return clone


def printState(state):
    # clone = copy.deepcopy(state)
    length = list(map(lambda x: len(x), state))
    clone = padding(state, [' '])
    # print(clone)
    state_np = np.array(clone)
    print()
    for i in range(max(length)):
        print(' '.join(str(v) for v in state_np[:3, i]))
    print('------')


def validMoves(state):
    length = list(map(lambda x: len(x), state))
    result = []
    for i in range(3):
        # check peg1
        if length[0] > 0:
            top = state[0][0]
            if length[1] == 0 or state[1][0] > top:
                result.append([1,2])
            if length[2] == 0 or state[2][0] > top:
                result.append([1,3])
        # check peg2
        if length[1] > 0:
            top = state[1][0]
            if length[0] == 0 or state[0][0] > top:
                result.append([2,1])
            if length[2] == 0 or state[2][0] > top:
                result.append([2,3])
        # check peg3
        if length[2] > 0:
            top = state[2][0]
            if length[0] == 0 or state[0][0] > top:
                result.append([3,1])
            if length[1] == 0 or state[1][0] > top:
                result.append([3,2])
        return result


def makeMove(state, move):
    clone = copy.deepcopy(state)
    print(state,move)
    top = clone[move[0]-1][0]
    if len(clone[move[1]-1]) == 0 or top < clone[move[1]-1][0]:
        clone[move[0] - 1].remove(top)
        clone[move[1]-1][:0] = [top]
    else:
        print("Higher value added on top of lower value.")
        return
    print(clone)
    return clone


def stateMoveTuple(state, move):
    # print (tuple(tuple(state[0]),tuple(state[1]),tuple(state[2])),tuple(move)))
    return tuple((tuple((tuple(state[0]),tuple(state[1]),tuple(state[2]))),tuple(move)))


def epsilonGreedy(epsilon, Q, state, validMoves):
    global gm, rm
    valid_moves = validMoves(state)
    if  np.random.uniform()< epsilon:
        # Random Move
        rm +=1
        return valid_moves[np.random.choice(len(valid_moves))]
    else:
        # Greedy Move
        gm +=1
        Qs = np.array([Q.get(stateMoveTuple(state,m), -1) for m in valid_moves])
        return valid_moves[np.argmin(Qs)]


def trainQ(nRepetitions, learningRate, epsilonDecayFactor, validMoves, makeMove,disk=3):
    epsilon = 1.0
    # graphics = True
    # showMoves = not graphics
    # outcomes = np.zeros(nRepetitions)
    epsilons = np.zeros(nRepetitions)
    Q = {}
    steps = []
    for nGames in range(nRepetitions):
        epsilon *= epsilonDecayFactor
        epsilons[nGames] = epsilon
        step = 0
        # state = [[1,2,3],[],[]]
        val = []
        for i in range(disk):
            val.append(i + 1)
            state = [val, [], []]
            goal = [[], [], val]
        done = False

        while not done:
            step += 1
            move = epsilonGreedy(epsilon, Q, state,validMoves)
            stateNew = makeMove(state,move)
            # print(stateMoveTuple(state, move))
            if stateMoveTuple(state,move) not in Q:
                Q[stateMoveTuple(state,move)] = -1  # initial Q value for new board,move

            # if stateNew == [[],[],[1,2,3]]:
            if stateNew == goal:
                # print(stateNew == [[],[],[1,2,3]])
                Q[stateMoveTuple(state,move)] = 0
                # TDError = (1 - Q[stateMoveTuple(stateOld,moveOld)])
                # Q[stateMoveTuple(stateOld, moveOld)] += learningRate * TDError
                done = True
                # outcomes[nGames] = 1

            if step > 1:
                # TDError = (1 + Q.get(stateMoveTuple(state,move)) - Q.get(stateMoveTuple(stateOld,moveOld)))
                TDError = (1 + Q[stateMoveTuple(state,move)] - Q[stateMoveTuple(stateOld,moveOld)])
                Q[stateMoveTuple(stateOld, moveOld)] += learningRate * TDError

            stateOld, moveOld = state, move  # remember board and move to Q(board,move) can be updated after next steps
            state = stateNew
        steps.append(step)
    # print(epsilons)
    return (Q,np.array(steps))


def testQ(Q, maxSteps, validMoves, makeMove,disk=3):
    # state = [[1,2,3],[],[]]
    val = []
    for i in range(disk):
        val.append(i+1)
        state = [val,[],[]]
        goal = [[],[],val]
    step = 0
    states = [state]
    while step < maxSteps and state!=goal:
        move = epsilonGreedy(0, Q, state,validMoves)
        state = makeMove(state, move)
        states.append(state)
        step += 1
    # if state !=[[],[],[1,2,3]]:
    if state !=goal:
        return "Insufficient iteration to reach goal. Increase the iteration."
    return states


import matplotlib.patches as mpatch
import matplotlib.pyplot as plt
# % matplotlib inline


def draw(plist):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    height = 0.5
    color = ["purple", "red", "green", "grey", "yellow"]
    idx = 0
    rod_l = list(map(lambda x: max(x) if len(x) > 0 else 0, plist))
    rod = []
    xr = 2
    factor = 2 + 0.8 * (max(rod_l) - 1)
    for l in range(3):
        rod.append(xr)
        xr += factor
    print(rod)
    ax.set_xlim([-2, 15])
    ax.set_ylim([0, 3])
    r_ht = max(rod_l) * 0.5 + 0.5
    ax.add_patch(mpatch.Rectangle((rod[0], 0), .08, r_ht, facecolor="orange"))
    ax.add_patch(mpatch.Rectangle((rod[1], 0), .08, r_ht, facecolor="orange"))
    ax.add_patch(mpatch.Rectangle((rod[2], 0), .08, r_ht, facecolor="orange"))
    ax.add_patch(mpatch.Rectangle((-2, 0), 15, .02, facecolor="black"))

    for i in plist:
        if len(i) != 0:
            y = 0
            i.sort(reverse=True)
            for val in i:
                # x = rod[idx] - 0.4*val
                x = rod[idx] - 0.5 * val
                ax.add_patch(mpatch.Rectangle((x, y), val, height, facecolor=color[val - 1]))
                # ax.add_patch(mpatch.Rectangle((x, y),0.8*val,height,facecolor=color[val-1]))
                y += height
        idx += 1


a = [1, 2, 3]
a.sort(reverse=True)
# draw([[1, 3], [], [2]])


state0=[[1,2,3],[],[]]
# state1 = [[1],[2,3],[]]
# state2=[[3],[1],[2]]
# state3=[[3,4,5],[1,2],[6,7]]
# goal=[[], [], [1, 2, 3]]
# epsilonGreedy(0.8, Q, state0)
# Q, steps = trainQ(500, 0.2, 0.99, validMoves, makeMove)
gm =0
rm = 0
Q, steps = trainQ(1000, 0.5, 0.7, validMoves, makeMove,3)
print(min(steps))
# print(steps)
print(len(Q),gm,rm)
states = testQ(Q, 200, validMoves, makeMove,3)
print (states)
# for state in states:
#     printState(state)
# printState(state3)
# move = validMoves(state0)
# move = makeMove(state,[1,2])
# print(move)
# print(stateMoveTuple(state1,[1,2]))