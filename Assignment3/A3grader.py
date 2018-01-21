from A3 import *
from A2mysolution import *

# Delete all variables defined so far (in notebook)
for name in dir():
    if not callable(globals()[name]) and not name.startswith('_'):
        del globals()[name]

# import numpy as np
import os
import copy

g = 0

for func in ['aStarSearch', 'iterativeDeepeningSearch',
             'actionsF_8p', 'takeActionF_8p', 'goalTestF_8p',
             'runExperiment']:
    if func not in dir() or not callable(globals()[func]):
        print('CRITICAL ERROR: Function named \'{}\' is not defined'.format(func))
        print('  Check the spelling and capitalization of the function name.')


print('\nTesting actionsF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8])')
acts = actionsF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8])
correct = [('left', 1), ('right', 1), ('up', 1)]
if acts == correct:
    g += 5
    print('\n--- 5/5 points. Your actionsF_8p correctly returned', acts)
else:
    print('\n--- 0/5 points. Your actionsF_8p should have returned', correct, 'but you returned', acts)

print('\nTesting takeActionF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8], (''up'', 1))')
s = takeActionF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8], ('up', 1))
correct = ([1, 2, 3, 4, 0, 6, 7, 5, 8], 1)
if s == correct:
    g += 5
    print('\n--- 5/5 points. Your takeActionsF_8p correctly returned', s)
else:
    print('\n--- 0/5 points. Your takeActionsF_8p should have returned', correct, 'but you returned', s)

print('\nTesting goalTestF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8], [1, 2, 3, 4, 5, 6, 7, 0, 8])')
s = takeActionF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8],'up')
correct = [1, 2, 3, 4, 0, 6, 7, 5, 8]
if goalTestF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8], [1, 2, 3, 4, 5, 6, 7, 0, 8]):
    g += 5
    print('\n--- 5/5 points. Your goalTestF_8p correctly True')
else:
    print('\n--- 0/5 points. Your goalTestF_8p did not return True')


print('\nTesting aStarSearch([1, 2, 3, 4, 5, 6, 7, 0, 8],')
print('                     actionsF_8p, takeActionF_8p,')
print('                     lambda s: goalTestF_8p(s, [0, 2, 3, 1, 4,  6, 7, 5, 8]),')
print('                     lambda s: h1_8p(s, [0, 2, 3, 1, 4,  6, 7, 5, 8]))')

path = aStarSearch([1, 2, 3, 4, 5, 6, 7, 0, 8], actionsF_8p, takeActionF_8p,
                   lambda s: goalTestF_8p(s, [0, 2, 3, 1, 4,  6, 7, 5, 8]),
                   lambda s: h1_8p(s, [0, 2, 3, 1, 4,  6, 7, 5, 8]))


                   

correct = ([[1, 2, 3, 4, 5, 6, 7, 0, 8], [1, 2, 3, 4, 0, 6, 7, 5, 8], [1, 2, 3, 0, 4, 6, 7, 5, 8], [0, 2, 3, 1, 4, 6, 7, 5, 8]], 3)
if path == correct:
    g += 20
    print('\n--- 20/20 points. Your search correctly returned', path)
else:
    print('\n---  0/20 points. Your search should have returned', correct, 'but you returned', path)

print('\nTesting iterativeDeepeningSearch([5, 2, 8, 0, 1, 4, 3, 7, 6], ')
print('                                 [0, 2, 3, 1, 4,  6, 7, 5, 8],')
print('                                 actionsF_8p, takeActionF_8p, 10)')
path = iterativeDeepeningSearch([5, 2, 8, 0, 1, 4, 3, 7, 6],[0, 2, 3, 1, 4,  6, 7, 5, 8], actionsF_8p, takeActionF_8p, 10)
if type(path) == str and path.lower() == 'cutoff':
    g += 15
    print('\n--- 15/15 points. Your search correctly returned', path)
else:
    print('\n---  0/15 points. Your search should have returned ''cutoff'', but you returned', path)

print('\n{} Grade is {}/50'.format(os.getcwd().split('/')[-1], g))

