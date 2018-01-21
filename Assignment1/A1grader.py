# Delete all variables defined so far (in notebook)
for name in dir():
    if not callable(globals()[name]) and not name.startswith('_'):
        del globals()[name]

# import numpy as np
import os
import copy

# import A1mysolution as mine
# import imp
# imp.reload(mine)
# breadthFirstSearch = mine.breadthFirstSearch
# depthFirstSearch = mine.depthFirstSearch

# trainValidateTestKFolds = mine.trainValidateTestKFolds
# trainLinear = mine.trainLinear
# evaluateLinear = mine.evaluateLinear
# trainNN = mine.trainNN
# evaluateNN = mine.evaluateNN

# import neuralnetworks as nn

# def within(correct, attempt, diff):
#     return np.abs((correct-attempt) / correct)  < diff

g = 0

for func in ['breadthFirstSearch', 'depthFirstSearch']:
    if func not in dir() or not callable(globals()[func]):
        print('CRITICAL ERROR: Function named \'{}\' is not defined'.format(func))
        print('  Check the spelling and capitalization of the function name.')

def chuck1():
    global g

    succs = {'a': ['b'], 'b':['c', 'd'], 'c':['e'], 'd':['f', 'i'], 'e':['g', 'h', 'i']}
    print('Searching this graph:\n', succs)
    def succsf(s):
        return copy.copy(succs.get(s,[]))

    print('Looking for path from a to b.')
    bfsCorrect = ['a', 'b']
    dfsCorrect = ['a', 'b']
    bfs = breadthFirstSearch('a', 'b', succsf)
    dfs = depthFirstSearch('a', 'b', succsf)
    
    if bfs == bfsCorrect:
        g += 20
        print('20/20 points. Your breadthFirstSearch found correct solution path of',bfs)
    else:
        print(' 0/20 points. Your breadthFirstSearch did not find correct solution path of',bfsCorrect)

    if dfs == dfsCorrect:
        g += 20
        print('20/20 points. Your depthFirstSearch found correct solution path of',dfs)
    else:
        print(' 0/20 points. Your depthFirstSearch did not find correct solution path of',dfsCorrect)

    print('Looking for path from a to i.')
    bfsCorrect = ['a', 'b', 'd', 'i']
    dfsCorrect = ['a', 'b', 'c', 'e', 'i']
    bfs = breadthFirstSearch('a', 'i', succsf)
    dfs = depthFirstSearch('a', 'i', succsf)
    if bfs == bfsCorrect:
        g += 20
        print('20/20 points. Your breadthFirstSearch found correct solution path of',bfs)
    else:
        print(' 0/20 points. Your breadthFirstSearch did not find correct solution path of',bfsCorrect)
    if dfs == dfsCorrect:
        g += 20
        print('20/20 points. Your depthFirstSearch found correct solution path of',dfs)
    else:
        print(' 0/20 points. Your depthFirstSearch did not find correct solution path of',dfsCorrect)

chuck1()

print('\n{} Grade is {}/100'.format(os.getcwd().split('/')[-1], g))
print('Up to 20 more points will be given based on the qualty of your descriptions of the method and the results.')
