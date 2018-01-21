#!/usr/bin/python
def ebf(nNodes, depth, precision=0.01):
    if nNodes == 0:
        return 0

    def ebfRec(low, high):
        mid = (low + high) * 0.5
        if mid == 1:
            estimate = 1 + depth
        else:
            estimate = (1 - mid**(depth + 1)) / (1 - mid)
        if abs(estimate - nNodes) < precision:
            return mid
        if estimate > nNodes:
            return ebfRec(low, mid)
        else:
            return ebfRec(mid, high)

    return ebfRec(1, nNodes)

# def negamaxIDS(startState, goalState, actionsF, takeActionF, maxDepth):

def negamaxIDS(game, depthLeft):
    # Initialize an empty best moves and score value.
    bestValue, bestMove = None, None
    for depth in range(depthLeft+1):
        value,move = negamax(game,depth)
        if game.getWinningValue() == value:
            return value, move # Winning step found so break out of further search.
        # Return the most possible value that can be achieved
        if bestValue is None or bestValue < value:
            bestValue = value
            bestMove = move
    return bestValue, bestMove

def negamaxIDSab(game, depthLeft):
    bestValue, bestMove = None, None
    for depth in range(depthLeft+1):
        value,move = negamaxAB(game,depth)
        if game.getWinningValue() == value:
            return value, move # Winning step found so break out of further search.
        # Return the most possible value that can be achieved
        if bestValue is None or bestValue < value:
            bestValue = value
            bestMove = move
    return bestValue, bestMove


def negamaxAB(game, depthLeft, alpha=-float('inf'), beta=float('inf')):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamaxAB(game, depthLeft-1, -beta, -alpha)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if bestValue is None or value > bestValue:
            bestValue = value
            bestMove = move
        alpha = max(bestValue, alpha)
        if beta <= bestValue:
            break
    return bestValue, bestMove

def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None # call to negamax knows the move
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
    return bestValue, bestMove

class TTT(object):

    def __init__(self):
        self.board = [' ']*9
        self.player = 'X'
        if True:
            self.board = [' ', ' ', 'O', 'X', 'O', 'O', ' ', ' ', ' ']
            self.player = 'O'
        self.playerLookAHead = self.player
        self.movesExplored = 0

    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    def getMoves(self):
        moves = self.locations(' ')
        return moves

    def getUtility(self):
        whereX = self.locations('X')
        whereO = self.locations('O')
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]
        isXWon = any([all([wi in whereX for wi in w]) for w in wins])
        isOWon = any([all([wi in whereO for wi in w]) for w in wins])
        if isXWon:
            return 1 if self.playerLookAHead is 'X' else -1
        elif isOWon:
            return 1 if self.playerLookAHead is 'O' else -1
        elif ' ' not in self.board:
            return 0
        else:
            return None  ########################################################## CHANGED FROM -0.1

    def isOver(self):
        return self.getUtility() is not None

    def makeMove(self, move):
        self.board[move] = self.playerLookAHead
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        self.movesExplored += 1

    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player

    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s

    def getNumberMovesExplored(self):
        return self.movesExplored

    def getWinningValue(self):
        return 1

def opponent(board):
    return board.index(' ')


def play(game,opponent,depthLimit,func):
    while not game.isOver():
        score,move = func(game,depthLimit)
        if move == None :
            print('move is None. Stopping.')
            break
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score' ,score)
        print(game)
        if not game.isOver():
            game.changePlayer()
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)   ### FIXED ERROR IN THIS LINE!
            print(game)
            game.changePlayer()

game = TTT()
playGame(game,opponent,9)
print('Number of moves explored', game.getNumberMovesExplored())