"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    #Starts the variables
    number_of_Xs = 0
    number_of_Os = 0

    for row in board:
        for line in row:
            if line == "X":
                number_of_Xs += 1
            if line =="O":
                number_of_Os += 1
    #If the number of Xs is equal or less than the number of Os it means it is X's turn
    if number_of_Xs <= number_of_Os:
        return X
    #Else it is O's turn
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #Starts the set of actions as empty
    actions_set = set()

    #Checks for empty spaces in the board and add a tuple of (line, colummn) to the set
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == None:
                actions_set.add((i, j))
    
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Uses the deepcopy to copy the board
    copy_board = copy.deepcopy(board)
    #Check what player has the move
    player_move = player(board)
    #Line
    i = action[0]
    #Colummn
    j = action[1]
    #Put a X or a O in the specified position depending in wich player has the move
    copy_board[i][j] = player_move

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            if board[i][0] == O:
                return O
    
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            if board[0][j] == O:
                return O

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        if board[0][0] == O:
            return O
    
    if board[2][0] == board[1][1] == board[0][2]:
        if board[1][1] == X:
            return X
        if board[1][1] == O:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not actions(board):
        return True
    else: 
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0 


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return none
    if board == initial_state():
        return (random.randint(0, 2), random.randint(0, 2))

    if player(board) == X:
        value = -math.inf
        best_action = None
        for action in actions(board):
            min_val = min_value(result(board,action))
            if min_val > value:
                value = min_val
                best_action = action
    if player(board) == O:
        value = +math.inf
        best_action = None
        for action in actions(board):
            max_val = max_value(result(board,action))
            if max_val < value:
                value = max_val
                best_action = action
    return best_action

def min_value(board):
    """
    Returns the min value of the current board
    """
    if terminal(board):
        return utility(board)
    v = +math.inf
    for action in actions(board):
        temp = min(v, max_value(result(board,action)))
        if temp < v:
            v = temp
    return v

def max_value(board):
    """
    Returns the max value of the current board
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        temp = max(v, min_value(result(board,action)))
        if temp > v:
            v = temp
    return v
