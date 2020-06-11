# Demo

Here we demonstrate the calling of the functions we've implemented and make  
sure they behave the same as what required in the specifications. You may try  
to call `doctest` module for a fast check.

Let's import the `minesweeper` module first before testing them.

    >>> from minesweeper import *

-----

## `class Sentence`

### `Sentence.known_mines()`

Returns the set of all cells in `self.cells` known to be mines. From all  
information available within the class, the only case which the cells are  
known to be mines is when the number of mines (`self.count`) is larger than  
0 and is equal to the number of cells in `self.cells`; otherwise, none of  
them is known to be mine.

### `Sentence.known_safes()`

Returns the set of all cells in `self.cells` known to be safe. From all  
information available within the class, the only case which the cells are  
known to be safe is when the number of mines (`self.count`) is 0, then all  
the cells in `self.cells` are safe; otherwise, none of them is safe.

Let's test the above 2 functions together. First we define 4 `Sentence`.

    >>> s0 = Sentence({(0, 0), (0, 1), (0, 2)}, 0)
    >>> s1 = Sentence({(0, 0), (0, 1), (0, 2)}, 1)
    >>> s2 = Sentence({(0, 0), (0, 1), (0, 2)}, 2)
    >>> s3 = Sentence({(0, 0), (0, 1), (0, 2)}, 3)

In `s0`, there's 0 mine in the cells. So all cells are safe.

    >>> s0.known_mines() == set()
    True
    >>> s0.known_safes() == {(0, 0), (0, 1), (0, 2)}
    True

In `s1`, there's 1 mine within the 3 cells, but we don't know which. So,  
nothing could be concluded.

    >>> s1.known_mines() == set()
    True
    >>> s1.known_safes() == set()
    True

In `s3`, there's 3 mine within the 3 cells. So all cells are mines.

    >>> s3.known_mines() == {(0, 0), (0, 1), (0, 2)}
    True
    >>> s3.known_safes() == set()
    True

### `Sentence.mark_mine(cell)`

If the given `cell` is in the sentence, the function should update the  
sentence so that cell is no longer in the sentence, but still represents a  
logically correct sentence given that cell is known to be a mine. Precisely,  
remove `cell` from `self.cell`, and subtract 1 from `self.count`.

Let's mark a cell which is not in the sentence as mine.

    >>> s2.mark_mine((1, 1))
    >>> s2 == Sentence({(0, 0), (0, 1), (0, 2)}, 2)
    True

Meaning that nothing is changed.

Now, let's mark the middle one as mine.

    >>> s2.mark_mine((0, 1))
    >>> s2 == Sentence({(0, 0), (0, 2)}, 1)
    True

The given cell has been removed, and `self.count` has been decreased by 1.

### `Sentence.mark_safe(cell)`

If the given `cell` is in the sentence, the function should update the  
sentence so that cell is no longer in the sentence, but still represents a  
logically correct sentence given that cell is known to be safe. Precisely,  
remove `cell` from `self.cell`, while keeps `self.count` unchanged.

Let's mark a cell which is not in the sentence as safe.

    >>> s1.mark_safe((1, 1))
    >>> s1 == Sentence({(0, 0), (0, 1), (0, 2)}, 1)
    True

Meaning that nothing is changed.

Now, let's mark the middle one as safe.

    >>> s1.mark_safe((0, 1))
    >>> s1 == Sentence({(0, 0), (0, 2)}, 1)
    True

The given cell has been removed, and `self.count` remains unchanged (1).

-----

## `class MinesweeperAI`

### `MinesweeperAI.make_safe_move()`

Returns a safe cell to choose on the Minesweeper board. The move must be  
known to be safe, and not already a move that has been made. We are allowed  
to use the knowledge in self.mines, self.safes and self.moves_made, but  
should not modify any of those values. So, the return should be:

> &lt;safes&gt; - &lt;moves made&gt;

Let's test the functions. Say we have the following board:

|R\C|`0`|`1`|`2`|`3`|
|:-:|:-:|:-:|:-:|:-:|
|`0`| 0 | S |   |   |
|`1`| S | 2 |   |   |
|`2`| M |   |   |   |
|`3`|   |   |   |   |

- _Numbers_ are moves made, indicating the count of neighboring mines
- "S" are the safes
- "M" are the mines
- _Empty grids_ are unexplored cells

We initialize an `MinesweeperAI` object according to the above board setting.

    >>> ai = MinesweeperAI(4, 4)
    >>> ai.mines = {(2, 0)}
    >>> ai.safes = {(0, 0), (0, 1), (1, 0), (1, 1)}
    >>> ai.moves_made = {(0, 0), (1, 1)}
    >>> ai.knowledge = [
    ...     Sentence({(0, 2), (1, 2), (2, 1), (2, 2)}, 1) 
    ... ]

We make a deep-copy of our `ai` object for comparing.

    >>> import copy
    >>> ai_copy = copy.deepcopy(ai)

Let's call `MinesweeperAI.make_safe_move()` once, and check if any member  
variable has been changed after calling.

    >>> new_move = ai.make_safe_move()
    >>> ai.mines == ai_copy.mines
    True
    >>> ai.safes == ai_copy.safes
    True
    >>> ai.moves_made == ai_copy.moves_made
    True
    >>> ai.knowledge == ai_copy.knowledge
    True

Let's check if the cell returned is in `ai.safes` and not in `ai.moves_made`.

    >>> new_move in ai.safes
    True
    >>> new_move in ai.moves_made
    False

### `MinesweeperAI.make_random_move()`

Returns a move to make on the Minesweeper board. Should choose randomly among  
cells that:

1. have not already been chosen, and
2. are not known to be mines

So, the return should be:

> &lt;all cells&gt; - &lt;moves made&gt; - &lt;mines&gt;

Let's call `MinesweeperAI.make_random_move()` once, and check if any member  
variable has been changed after calling.

    >>> new_move = ai.make_random_move()
    >>> ai.mines == ai_copy.mines
    True
    >>> ai.safes == ai_copy.safes
    True
    >>> ai.moves_made == ai_copy.moves_made
    True
    >>> ai.knowledge == ai_copy.knowledge
    True

Let's check if the cell returned is not in `ai.moves_made` and not in  
`ai.mines`.

    >>> all_cells = [
    ...     (0, 0), (0, 1), (0, 2), (0, 3), 
    ...     (1, 0), (1, 1), (1, 2), (1, 3), 
    ...     (2, 0), (2, 1), (2, 2), (2, 3), 
    ...     (3, 0), (3, 1), (3, 2), (3, 3), 
    ... ]
    >>> new_move in all_cells
    True
    >>> new_move in ai.moves_made
    False
    >>> new_move in ai.mines
    False

### `MinesweeperAI.add_knowledge(cell, count)`

This function does a lot of work. Given that a new move has been made which  
is luckily not a mine, we input this cell and the number of mines we've  
revealed into the AI with this function. According to the specification,

1. The function should mark the cell as one of the moves made in the game.
2. The function should mark the cell as a safe cell, updating any sentences  
   that contain the cell as well.
3. The function should add a new sentence to the AI’s knowledge base, based  
   on the value of cell and count, to indicate that count of the cell’s  
   neighbors are mines. Be sure to only include cells whose state is still  
   undetermined in the sentence.
4. If, based on any of the sentences in self.knowledge, new cells can be  
   marked as safe or as mines, then the function should do so.
5. If, based on any of the sentences in self.knowledge, new sentences can be  
   inferred (using the subset method described in the Background), then those  
   sentences should be added to the knowledge base as well.

Let's try to make a safe move at (1, 0), which gives 2 neighboring mine. We  
expect,

1. (1, 0) is added in `ai.moves_made`.
2. As we're making a safe move, (1, 0) should surely be a member in  
   `ai.safes`.
3. New sentence should be made. But according to the board state, the move we  
   are going to add will identify all other neighboring cells. So after  
   removing determined cells from sentences, all sentences we've made will  
   become empty, and will be cleared immediately. So `ai.knowledge` will  
   become an empty `list`.
4. (0, 2), (1, 2) and (2, 2) should be added in `ai.safes`. (2, 1) should be  
   added in `ai.mines`.

Let's check if it matches our expectations.

    >>> ai.add_knowledge((1, 0), 2)
    >>> (1, 0) in ai.moves_made
    True
    >>> (1, 0) in ai.safes
    True
    >>> ai.knowledge == list()
    True
    >>> {(0, 2), (1, 2), (2, 2)} <= ai.safes
    True
