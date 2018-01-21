import copy

successors = {'a':  ['b', 'c', 'd'],
              'b':  ['c', 'e'],
              'c':  ['e'],
              'd':  ['c','f'],
              'e':  ['a'],
              'f':  ['c'],
              'g':['d','f','h'],
              'h':  ['c']}
# successors = {'a':  ['b', 'c', 'd'],
#               'b':  ['e', 'f', 'g'],
#               'c':  ['a', 'h', 'i'],
#               'd':  ['j', 'z'],
#               'e':  ['k', 'l'],
#               'g':  ['m'],
#               'k':  ['z']}

def successorsf(state):
    return copy.deepcopy(successors.get(state, []))

# def breadthFirstSearch(startState, goalState, successorsf):
#     expanded = {}
#     unExpanded = [(startState, None)]
#     breadthFirst = True
#     while len(unExpanded) != 0:
#         state, parent = unExpanded.pop()
#         print("Unexpanded after pop={}".format(unExpanded))
#         # print("State:parent={}:{}".format(state, parent))
#         children = successorsf(state)
#         # print("children value returned={}".format(children))
#         expanded.update({state: parent})
#         print("Expanded added with new pair={}".format(expanded))
#         if state== goalState:
#             # print("Goal found!!")
#             break
#             # Remove from children any states that are already in expanded or unExpanded.
#
#         children.sort(reverse=True)
#         # children.reverse()
#         # print("Children value sorted and reversed: {}".format(children))
#
#         childstate = [(child, state) for child in children]
#         # print("Childstate={}".format(childstate))
#         # Create a modified children list by changing each entry to be a pair (child, parent),
#         #  where parent is the parent of the child.
#         # if breadthFirst:
#         #     for child in childstate:
#         #         unExpanded.insert(0,child)
#         # else:
#         #     for child in childstate:
#         #         unExpanded.insert(len(unExpanded),child)
#         # # print("=>Final UE={}\n=>Final EX={}".format(unExpanded,expanded))
#         if breadthFirst:
#             unExpanded[:0] = childstate
#         else:
#             unExpanded.extend(childstate)
#     if goalState in expanded:
#         solutionPath = [state]
#         # print("SolutionPath: {}".format(solutionPath))
#         while parent:
#             solutionPath.insert(0,parent)
#             parent = expanded[parent]
#             # print("Inside loop. solutionPath={}, parent={}".format(solutionPath,parent))
#             #set parent to the parent of parent.
#         return solutionPath
#     else:
#         return ["Goal not found!"]




def breadthFirstSearch(startState, goalState, successorsf):
    expanded = {}
    unExpanded = [(startState, None)]
    breadthFirst = True
    while len(unExpanded) != 0:
        state, parent = unExpanded.pop()
        try:
            print("Get camelsuccessor for {}".format(state))
            children = successorsf(state)
        except:
            continue
        expanded.update({state: parent})
        # print ("EX={}\nUEx={}".format(expanded,unExpanded))
        if state == goalState:
            break

        children.sort(reverse=True)
        childstate = [(child, state) for child in children if child not in expanded]
        print("Childstate:{}".format(childstate))
        # Create a modified children list by changing each entry to be a pair (child, parent),
        #  where parent is the parent of the child.
        if breadthFirst:
            unExpanded[:0] = childstate
        else:
            unExpanded.extend(childstate)
    if goalState in expanded:
        solutionPath = [state]
        while parent:
            solutionPath.insert(0, parent)
            parent = expanded[parent]
            # set parent to the parent of parent.
        return solutionPath
    else:
        return ["Goal not found in given tree!"]


def depthFirstSearch(startState, goalState, successorsf):
    breadthFirst = False
    expanded = {}
    unExpanded = [(startState, None)]

    while len(unExpanded) != 0:
        state, parent = unExpanded.pop()
        # print ("UE:{}\n len(UE)={}".format(unExpanded,len(unExpanded)))
        try:
            children = successorsf(state)
        except:
            print("Error retrieving child.")
            continue
        expanded.update({state: parent})
        if state == goalState:
            break

        children.sort(reverse=True)
        childstate = [(child, state) for child in children if child not in expanded]
        # Create a modified children list by changing each entry to be a pair (child, parent),
        #  where parent is the parent of the child.
        if breadthFirst:
            unExpanded[:0] = childstate
        else:
            unExpanded.extend(childstate)


    if goalState in expanded:
        solutionPath = [state]
        while parent:
            solutionPath.insert(0, parent)
            parent = expanded[parent]
            # set parent to the parent of parent.
        return solutionPath
    else:
        return ["Goal not found in given tree!"]


def camelSuccessorsf(state):
    position = state.index(' ')
    output = []
    # RR_
    if state[position-1]=='R' and state[position-2]=='R':
        # print("RR_")
        stateList = list(state)
        stateList[position-1],stateList[position] = stateList[position],stateList[position-1]
        if tuple(stateList) not in output:
            output.append(tuple(stateList))

    # _RL
    if position < len(state) -2 and state[position+1]=='R' and state[position+2]=='L':
        # print("RL_")
        stateList = list(state)
        stateList[position],stateList[position+2] = stateList[position+2],stateList[position]
        if tuple(stateList) not in output:
            output.append(tuple(stateList))

    #_LL
    if position < len(state)-2 and state[position+1]=='L' and state[position+2]=='L':
        # print("_LL")
        stateList = list(state)
        stateList[position],stateList[position+1] = stateList[position+1],stateList[position]
        if tuple(stateList) not in output:
            output.append(tuple(stateList))

    #RL_
    if state[position-1]=='L' and state[position-2]=='R':
        # print("RL_")
        stateList = list(state)
        stateList[position],stateList[position-2]= stateList[position-2],stateList[position]
        if tuple(stateList) not in output:
            output.append(tuple(stateList))

    # _LR
    if position < len(state)-2 and state[position+1]=='L' and state[position+2]=='R':
        # print ("_LR")
        stateList = list(state)
        stateList[position],stateList[position+1] = stateList[position+1],stateList[position]
        if tuple(stateList) not in output:
            output.append(tuple(stateList))

    #R_L
    if state[position-1] == 'R' and state[position+1]=='L':
        # print ("R_L")
        stateList = list(state)
        stateList[position+1],stateList[position] = stateList[position],stateList[position+1]
        if tuple(stateList) not in output:
            output.append(tuple(stateList))

    #LR_
    if state[position-2] == 'L' and state[position-1] == 'R':
        # print("LR_")
        stateList=list(state)
        stateList[position-1],stateList[position] = stateList[position],stateList[position-1]
        if tuple(stateList) not in output:
            output.append(tuple(stateList))

    # print ("Output:{}".format(output))
    return output


camelStartState=('R','R','R','R',' ', 'L','L','L','L')
state1=('L', 'L', 'R', 'L', 'R', 'L', ' ', 'R', 'R')
state2=('L', 'L', 'R', 'L', ' ', 'L', 'R', 'R', 'R')
camelGoalState=('L', 'L', 'L', 'L', ' ', 'R', 'R', 'R', 'R')
bfs = depthFirstSearch(camelStartState, camelGoalState, camel)
print('Breadth-first solution: (', len(bfs), 'steps)')
for s in bfs:
    print(s)
# a=('R', 'L', 'R', 'L', 'R', 'L', 'R', ' ', 'L')
# print (camel(a))