import os
import copy
import signal

# Code to limit running time of specific parts of code.
#  To use, do this for example...
#
#  signal.alarm(seconds)
#  try:
#    ... run this ...
#  except TimeoutException:
#     print(' 0/8 points. Your depthFirstSearch did not terminate in', seconds/60, 'minutes.')
# Exception to signal exceeding time limit.


class TimeoutException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def timeout(signum, frame):
    raise TimeoutException


signal.signal(signal.SIGALRM, timeout)


# Eval all function defs in students notebook. Assumes the following command
# has been executed.
#   jupyter nbconvert --to script *.ipynb --stdout > nbconvert.py

if True:
    import ast
    with open('nbconvert.py') as fp:
        tree = ast.parse(fp.read(), 'eval')
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            eval(compile(ast.Interactive(body=[node]), '', 'single'))
else:
    import A2mysolution as mine
    iterativeDeepeningSearch = mine.iterativeDeepeningSearch
    depthLimitedSearch = mine.depthLimitedSearch
    findBlank_8p = mine.findBlank_8p
    actionsF_8p = mine.actionsF_8p
    takeActionF_8p = mine.takeActionF_8p
    printPath_8p = mine.printPath_8p


g = 0

for func in ['iterativeDeepeningSearch', 'depthLimitedSearch',
             'findBlank_8p', 'actionsF_8p', 'takeActionF_8p', 'printPath_8p']:
    if func not in dir() or not callable(globals()[func]):
        print('CRITICAL ERROR: Function named \'{}\' is not defined'.format(func))
        print('  Check the spelling and capitalization of the function name.')

seconds = 60 * 5

succs = {'a': ['b', 'z', 'd'], 'b':['a'], 'e':['z'], 'd':['y'], 'y':['z'], 'z':['g']}
print('\nSearching this graph:\n', succs)
def aF(state):
    return copy.copy(succs.get(state,[]))
def tAF(state, action):
    return action
print('\nLooking for path from a to g with max depth of 1.')

signal.alarm(seconds)
try:
    path = iterativeDeepeningSearch('a', 'g', aF, tAF, 1)
    if type(path) == str and path.lower() == 'cutoff':
        g += 5
        print(' 5/ 5 points. Your search correctly returned', path)
    else:
        print(' 0/ 5 points. Your search should have returned ''cutoff''. You returned', path)

except TimeoutException:
    print('0/5 points. Your iterativeDeepeningSearch did not terminate in', seconds/60, 'minutes.')

except Exception:
    print('0/5 points. Your iterativeDeepeningSearch raised an exception.')


print('\nLooking for path from a to g with max depth of 5.')
signal.alarm(seconds)
try:
    path = iterativeDeepeningSearch('a', 'g', aF, tAF, 5)
    if path == ['a', 'z', 'g']:
        g += 10
        print('10/10 points. Your search correctly returned', path)
    else:
        print(' 0/10 points. Your search should have returned', ['a', 'g'])

except TimeoutException:
    print('0/10 points. Your iterativeDeepeningSearch did not terminate in', seconds/60, 'minutes.')

except Exception:
    print('0/10 points. Your iterativeDeepeningSearch raised an exception.')
    


print('\nTesting findBlank_8p([1, 2, 3, 4, 5, 6, 7, 0, 8])')
r, c = findBlank_8p([1, 2, 3, 4, 5, 6, 7, 0, 8])
if r == 2 and c == 1:
    g += 5
    print('5/5 points. Your findBlank_8p correctly returned', r, c)
else:
    print('0/5 points. Your findBlank_8p should have returned 2 1 but you returned', r, c)

print('\nTesting actionsF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8])')
acts = actionsF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8])
correct = ['left', 'right', 'up']
if acts == correct:
    g += 5
    print('5/5 points. Your actionsF_8p correctly returned', acts)
else:
    print('0/5 points. Your actionsF_8p should have returned', correct, 'but you returned', acts)

print('\nTesting takeActionF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8],\'up\')')
s = takeActionF_8p([1, 2, 3, 4, 5, 6, 7, 0, 8],'up')
correct = [1, 2, 3, 4, 0, 6, 7, 5, 8]
if s == correct:
    g += 5
    print('5/5 points. Your takeActionsF_8p correctly returned', s)
else:
    print('0/5 points. Your takeActionsF_8p should have returned', correct, 'but you returned', s)


print('\nTesting iterativeDeepeningSearch([1, 2, 3, 4, 5, 6, 7, 0, 8],[0, 2, 3, 1, 4,  6, 7, 5, 8], actionsF_8p, takeActionF_8p, 5)')
signal.alarm(seconds)
try:
    path = iterativeDeepeningSearch([1, 2, 3, 4, 5, 6, 7, 0, 8],[0, 2, 3, 1, 4,  6, 7, 5, 8], actionsF_8p, takeActionF_8p, 5)
    correct = [[1, 2, 3, 4, 5, 6, 7, 0, 8], [1, 2, 3, 4, 0, 6, 7, 5, 8], [1, 2, 3, 0, 4, 6, 7, 5, 8], [0, 2, 3, 1, 4, 6, 7, 5, 8]]
    if path == correct:
        g += 20
        print('20/20 points. Your search correctly returned', path)
    else:
        print('0/20 points. Your search should have returned', correct, 'but you returned', path)

except TimeoutException:
    print('0/20 points. Your iterativeDeepeningSearch did not terminate in', seconds/60, 'minutes.')

except Exception:
    print('0/20 points. Your iterativeDeepeningSearch raised an exception.')
    

print('\nTesting iterativeDeepeningSearch([5, 2, 8, 0, 1, 4, 3, 7, 6], [0, 2, 3, 1, 4,  6, 7, 5, 8], actionsF_8p, takeActionF_8p, 10)')
signal.alarm(seconds)
try:
    path = iterativeDeepeningSearch([5, 2, 8, 0, 1, 4, 3, 7, 6],[0, 2, 3, 1, 4,  6, 7, 5, 8], actionsF_8p, takeActionF_8p, 10)
    if type(path) == str and path.lower() == 'cutoff':
        g += 20
        print('20/20 points. Your search correctly returned', path)
    else:
        print('0/20 points. Your search should have returned ''cutoff'', but you returned', path)

except TimeoutException:
    print('0/20 points. Your iterativeDeepeningSearch did not terminate in', seconds/60, 'minutes.')

except Exception:
    print('0/20 points. Your iterativeDeepeningSearch raised an exception.')


print('\nTesting iterativeDeepeningSearch([0, 1, 5, 4, 3, 8, 6, 2, 7], [1, 2, 3, 4, 0, 5, 6, 7, 8], actionsF_8p, takeActionF_8p, 15)')
signal.alarm(seconds)
try:
    path = iterativeDeepeningSearch(
        [0, 1, 5, 4, 3, 8, 6, 2, 7],
        [1, 2, 3, 4, 0, 5, 6, 7, 8], actionsF_8p, takeActionF_8p, 15)
    if type(path) == list and len(path) == 9:
        g += 20
        print('20/20 points. Your search correctly returned', path)
    else:
        print('0/20 points. Your search should have returned a path of length 9')

except TimeoutException:
    print('0/20 points. Your iterativeDeepeningSearch did not terminate in', seconds/60, 'minutes.')

except Exception:
    print('0/20 points. Your iterativeDeepeningSearch raised an exception.')
    
name = os.getcwd().split('/')[-1]
print('\n{} Grade is {}/90'.format(name, g))
print('\n{} SECOND search problem grade is __/10'.format(name))
print('\n{} FINAL GRADE is __/100'.format(name))




