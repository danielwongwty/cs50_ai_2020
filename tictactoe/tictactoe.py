"""
Tic Tac Toe Player
"""

import math
import copy

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

    We determine by counting which mark has got less. It's the turn of 
    O player if there's less O mark then X mark; otherwise it's the turn of 
    X player.
    """
    count_X = 0
    count_O = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_X += 1
            elif board[i][j] == O:
                count_O += 1
    return O if count_O < count_X else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    It loops through the whole board and return the (i, j) tuple if its value 
    equals EMPTY.
    """
    return { (i, j) for i in range(3) for j in range(3) 
            if board[i][j] == EMPTY }


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action specified is valid
    row, col = action
    if board[row][col] != EMPTY:
        raise Exception("Invalid action. Cell specified is already marked.")

    current_player = player(board)

    # Deep-copy the current board and add a new move
    new_board = copy.deepcopy(board)
    new_board[row][col] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check horizontally
    for i in range(3):
        marks = {board[i][0], board[i][1], board[i][2]}
        if len(marks) == 1 and EMPTY not in marks:
            """ If there's only one type of mark, which is not EMPTY """
            return board[i][0]

    # Check vertically
    for j in range(3):
        marks = {board[0][j], board[1][j], board[2][j]}
        if len(marks) == 1 and EMPTY not in marks:
            return board[0][j]

    # Check diagonally
    marks = {board[0][0], board[1][1], board[2][2]}
    if len(marks) == 1 and EMPTY not in marks:
        return board[1][1]

    # Another diagonal
    marks = {board[0][2], board[1][1], board[2][0]}
    if len(marks) == 1 and EMPTY not in marks:
        return board[1][1]
    
    # If no winner is found
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return len(actions(board)) == 0 or winner(board) != None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return {X:      1, 
            O:      -1, 
            None:   0}[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def min_value(board, pruning_min=None):
        """
        Given a board for the turn of O player, return a (score, action) tuple 
        in which `score` is the minimum score among its possible actions, and 
        `action` is its corresponding action. If `pruning_min` is given, 
        instead of finding the minimum score, it stops when it find the first 
        occurance of action which has lower score than the given `pruning_min`.
        """

        if terminal(board):
            return utility(board), None

        possible_actions = actions(board)
        best_score = 10000
        best_action = None
        for a in possible_actions:
            score = max_value(result(board, a), best_score)[0]
            if score < best_score:
                best_score = score
                best_action = a
            if pruning_min is not None and best_score < pruning_min:
                break

        return best_score, best_action

    def max_value(board, pruning_max=None):
        """
        Given a board for the turn of X player, return a (score, action) tuple 
        in which `score` is the maximum score among its possible actions, and 
        `action` is its corresponding action. If `pruning_max` is given, 
        instead of finding the maximum score, it stops when it find the first 
        occurance of action which has higher score than the given 
        `pruning_max`.
        """

        if terminal(board):
            return utility(board), None

        possible_actions = actions(board)
        best_score = -10000
        best_action = None
        for a in possible_actions:
            score = min_value(result(board, a), best_score)[0]
            if score > best_score:
                best_score = score
                best_action = a
            if pruning_max is not None and best_score > pruning_max:
                break

        return best_score, best_action

    current_player = player(board)
    if current_player == X:
        """ Look for the move with largest score """
        return max_value(board)[1]
    else:
        """ Look for the move with smallest score """
        return min_value(board)[1]

