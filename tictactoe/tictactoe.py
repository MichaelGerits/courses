"""
Tic Tac Toe Player
"""

from cmath import inf
from copy import deepcopy
from random import randrange

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None
    #since X starts everytime there's an even amount of empty spaces it will be O's turn.
    emptyCount = 0
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                emptyCount += 1
    if emptyCount % 2 == 0:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #I would add a terminal check, but it works off the same principle so there's no need to do it twice.
    #goes by each cell on the board and if it's empty it adds it to the actions set which is then returned.
    actions = set()
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                actions.add((row, cell))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #makes sure that the action is even valid.
    if action not in actions(board):
        raise ValueError("invalid move")
    elif terminal(board):
        raise ValueError("Game Over.")
    else:
        #makes a copy of the board and only works of that to be sure
        current = player(board)
        boardCopy = deepcopy(board)
        #add the current player to the requested action/cell of the copy which it then returns, thus leaving the original unscathed.
        boardCopy[action[0]][action[1]] = current
        return boardCopy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #checks all possible winning situations for both players
    for player in [X, O]:
        #scans horizontally for a vertical win
        for collumn in range(3):
            if board[0][collumn] == player and board[1][collumn] == player and board[2][collumn] == player:
                return player
        #scans vertically for a horizontal win
        for row in board:
            if row.count(player) == 3:
                return player
        #check both of the diagonal wins.
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return player
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return player

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #by using the same method of actions but now the other way round it checks for any empty spaces.
    if winner(board) != None:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #pairs the winner to it's utility state
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif board == initial_state():
        return (randrange(0,3), randrange(0,3))

    currP = player(board)
    bestAction = None
    if currP == X:
        bestVal = float(-inf)
        for action in actions(board):
            if minVal(result(board, action)) >= bestVal:
                bestAction = action
                bestVal = minVal(result(board, action))
    else:
        bestVal = float(inf)
        for action in actions(board):
            if maxVal(result(board, action)) <= bestVal:
                bestAction = action
                bestVal = maxVal(result(board, action))
    return bestAction
    #raise NotImplementedError

def maxVal(board):
    if terminal(board):
        return utility(board)
    v = float(-inf)
    for action in actions(board):
        v = max(v, minVal(result(board, action)))
    return v

def minVal(board):
    if terminal(board):
        return utility(board)
    v = float(inf)
    for action in actions(board):
        v = min(v, maxVal(result(board, action)))
    return v
