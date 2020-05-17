# Demo

Here we demonstrate the calling of each function in `tictactoe` to make sure  
it sticks to the specification. You may try to call `doctest` module for a  
fast check.

Let's import the module and test it one by one.

    >>> from tictactoe import *

## `player(board)`

At the initial game state, X should get the first move:

    >>> player([[EMPTY, EMPTY, EMPTY], 
    ...         [EMPTY, EMPTY, EMPTY], 
    ...         [EMPTY, EMPTY, EMPTY]]) == X
    True

Subsequently, the player alternates with each additional move:

    >>> player([[EMPTY, EMPTY, EMPTY], 
    ...         [EMPTY,   X  , EMPTY], 
    ...         [EMPTY, EMPTY, EMPTY]]) == O
    True

    >>> player([[EMPTY, EMPTY,   O  ], 
    ...         [EMPTY,   X  , EMPTY], 
    ...         [EMPTY, EMPTY, EMPTY]]) == X
    True

## `actions(board)`

For empty board, tuples of all position should be returned in a `set`:

    >>> rtn = actions([[EMPTY, EMPTY, EMPTY], 
    ...                [EMPTY, EMPTY, EMPTY], 
    ...                [EMPTY, EMPTY, EMPTY]])
    >>> type(rtn)
    <class 'set'>
    >>> rtn == {(0, 0), (0, 1), (0, 2), 
    ...         (1, 0), (1, 1), (1, 2), 
    ...         (2, 0), (2, 1), (2, 2)}
    True

Only empty cells should be returned:

    >>> actions([[  O  , EMPTY, EMPTY], 
    ...          [EMPTY,   X  , EMPTY], 
    ...          [EMPTY, EMPTY, EMPTY]]) == {        (0, 1), (0, 2), 
    ...                                      (1, 0),         (1, 2), 
    ...                                      (2, 0), (2, 1), (2, 2)}
    True

For a fully occupied board, an empty `set` should be returned:

    >>> actions([[  O  ,   X  ,   O  ], 
    ...          [  O  ,   X  ,   X  ], 
    ...          [  X  ,   O  ,   X  ]]) == set()
    True

## `result(board, action)`

It should return a new board state, without modifying the original board.  
Say we try to add a move to (1, 1) position of an empty board:

    >>> before = [[EMPTY, EMPTY, EMPTY], 
    ...           [EMPTY, EMPTY, EMPTY], 
    ...           [EMPTY, EMPTY, EMPTY]]
    >>> result(before, (1, 1)) == [[EMPTY, EMPTY, EMPTY], 
    ...                            [EMPTY,   X  , EMPTY], 
    ...                            [EMPTY, EMPTY, EMPTY]]
    True

A mark has been added at expected position according to the given `action`.  
Now, let's check the original board. It should still be an empty board.

    >>> before == [[EMPTY, EMPTY, EMPTY], 
    ...            [EMPTY, EMPTY, EMPTY], 
    ...            [EMPTY, EMPTY, EMPTY]]
    True

If the action is invalid for the board, an `Exception` will be raised:

    >>> before = [[  O  , EMPTY, EMPTY], 
    ...           [EMPTY,   X  , EMPTY], 
    ...           [EMPTY, EMPTY, EMPTY]]
    >>> result(before, (0, 0))
    Traceback (most recent call last):
        ...
    Exception: Invalid action. Cell specified is already marked.

## `winner(board)`

Let's check several cases.

Horizontally:

    >>> winner([[  X  ,   O  , EMPTY], 
    ...         [  X  ,   X  ,   X  ], 
    ...         [  O  , EMPTY,   O  ]]) == X
    True

Vertically:

    >>> winner([[  O  ,   O  ,   X  ], 
    ...         [EMPTY,   X  ,   X  ], 
    ...         [  O  , EMPTY,   X  ]]) == X
    True

Diagonally:

    >>> winner([[  O  ,   X  ,   X  ], 
    ...         [EMPTY,   O  , EMPTY], 
    ...         [EMPTY,   X  ,   O  ]]) == O
    True

Another diagonal:

    >>> winner([[  O  , EMPTY,   X  ], 
    ...         [  O  ,   X  , EMPTY], 
    ...         [  X  , EMPTY, EMPTY]]) == X
    True

No winner is found:

    >>> winner([[EMPTY, EMPTY, EMPTY], 
    ...         [EMPTY,   X  , EMPTY], 
    ...         [EMPTY, EMPTY, EMPTY]]) == None
    True

## `terminal(board)`

It should return `True` if someone wins the game.

    >>> terminal([[  X  ,   O  , EMPTY], 
    ...           [  X  ,   X  ,   X  ], 
    ...           [  O  , EMPTY,   O  ]])
    True

It should return `True` if all cells have been filled without anyone winning.

    >>> terminal([[  O  ,   X  ,   O  ], 
    ...           [  O  ,   X  ,   X  ], 
    ...           [  X  ,   O  ,   X  ]])
    True

It should return `False` if the game is still in progress.

    >>> terminal([[  O  , EMPTY, EMPTY], 
    ...           [EMPTY,   X  , EMPTY], 
    ...           [EMPTY, EMPTY, EMPTY]])
    False

## `utility(board)`

It should returns 1 if X wins.

    >>> utility([[  X  ,   O  , EMPTY], 
    ...          [  X  ,   X  ,   X  ], 
    ...          [  O  , EMPTY,   O  ]])
    1

It should returns -1 if O wins.

    >>> utility([[  O  ,   X  ,   X  ], 
    ...          [EMPTY,   O  , EMPTY], 
    ...          [EMPTY,   X  ,   O  ]])
    -1

It should return 0 if the game has ended in a tie.

    >>> utility([[  O  ,   X  ,   O  ], 
    ...          [  O  ,   X  ,   X  ], 
    ...          [  X  ,   O  ,   X  ]])
    0

## `minimax(board)`

The move returned should be the optimal action `(i, j)` that is one of the  
allowable actions on the board. Let's check if it returns a single action  
(a `tuple` of `size == 2`).

    >>> rtn = minimax([[EMPTY, EMPTY, EMPTY], 
    ...                [EMPTY, EMPTY, EMPTY], 
    ...                [EMPTY, EMPTY, EMPTY]])
    >>> type(rtn)
    <class 'tuple'>
    >>> len(rtn)
    2

If the `board` is a terminal board, it should return `None`.

    >>> minimax([[  X  ,   O  , EMPTY], 
    ...          [  X  ,   X  ,   X  ], 
    ...          [  O  , EMPTY,   O  ]]) == None    # Someone wins
    True

    >>> minimax([[  O  ,   X  ,   O  ], 
    ...          [  O  ,   X  ,   X  ], 
    ...          [  X  ,   O  ,   X  ]]) == None    # The board is full
    True
