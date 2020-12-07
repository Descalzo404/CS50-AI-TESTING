import math
import copy

X = "X"
O = "O"
EMPTY = None

board = [[O, X, O],
        [X, X, O],
        [O, O, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    number_of_Xs = 0
    number_of_Os = 0
    for row in board:
        for line in row:
            if line == "X":
                number_of_Xs += 1
            if line =="O":
                number_of_Os += 1
    if number_of_Xs > number_of_Os:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == None:
                actions_set.add((i, j))
    return actions_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    player_move = player(board)
    i = action[0]
    j = action[1]
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

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return none
    if player(board) == X:
        action = max_value(board)[1]
        return action
    if player(board) == O:
        action = min_value(board)[1]
        return action

def min_value(board):
    """
    Returns the min value of the current board
    """
    if terminal(board):
        return utility(board)
    v = +1
    for action in actions(board):
        v = min(v, max_value(result(board,action)))
        if temp < v:
            v = temp
            move = action
    return (v, move)

def max_value(board):
    """
    Returns the max value of the current board
    """
    move = None
    if terminal(board):
        return utility(board)
    v = -1
    for action in actions(board):
        temp = max(v, min_value(result(board,action)))
        if temp > v:
            v = temp
            move = action
    return (v, move)