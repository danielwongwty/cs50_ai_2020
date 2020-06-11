import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count > 0 and len(self.cells) <= self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells:
            return
        self.cells.remove(cell)
        self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell not in self.cells:
            return
        self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Initialize some internal variables
        new_sentences = []
        known_mines = set()
        known_safes = set()

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe, update existing sentences as well
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`

        #    3.1) Find its neighbors
        i_bounds = max(cell[0]-1, 0), min(cell[0]+2, self.height)
        j_bounds = max(cell[1]-1, 0), min(cell[1]+2, self.width)
        neighbors = { (i, j) for i in range(i_bounds[0], i_bounds[1])
            for j in range(j_bounds[0], j_bounds[1]) 
            if not (i == cell[0] and j == cell[1]) }
        
        #    3.2) Make a sentence, with determined cells removed
        new_sentence = Sentence(neighbors, count)
        for c in neighbors & self.mines:
            new_sentence.mark_mine(c)
        for c in neighbors & self.safes:
            new_sentence.mark_safe(c)

        #    3.3) Append into our internal variable, which is for 
        #         adding into knowledge base
        new_sentences.append(new_sentence)

        loopCount = 0

        while True:
            """ This loop continuously adds new sentences and make inferences 
            until no more inference could be made. """

            if (len(new_sentences) == 0 and 
                len(known_mines) == 0 and 
                len(known_safes) == 0):
                break

            loopCount += 1
            if loopCount > 5:
                print("Break due to max looping exceed")
                break

            #    3.4) Add all new_sentences into the knowledge base
            self.knowledge.extend(new_sentences)

            # 4) mark any additional cells as safe or as mines
            #    if it can be concluded based on the AI's knowledge base
            known_mines = set().union(
                            *(s.known_mines() for s in self.knowledge)
                            )
            for mine in known_mines:
                self.mark_mine(mine)
            known_safes = set().union(
                            *(s.known_safes() for s in self.knowledge)
                            )
            for safe in known_safes:
                self.mark_safe(safe)

            #    4.1) To optimize our loop, remove any empty sentence in our 
            #         knowledge base
            self.knowledge = [s for s in self.knowledge if len(s.cells)]

            # 5) add any new sentences to the AI's knowledge base
            #    if they can be inferred from existing knowledge
            #    (shorten the sentence if any other sub-sentence is found)
            new_sentences = []
            sentences_being_shortened = set()
            for id_1 in range(len(self.knowledge)):
                for id_2 in range(len(self.knowledge)):
                    if id_1 == id_2:
                        continue
                    s1 = self.knowledge[id_1]
                    s2 = self.knowledge[id_2]
                    if s1.cells <= s2.cells:
                        # This is the shortened sentence
                        new_sentences.append(Sentence(
                            s2.cells - s1.cells, 
                            s2.count - s1.count
                        ))
                        # Store the sentence id
                        sentences_being_shortened.add(id_2)
            # Remove the old sentence, since we have the new sentence now
            for id in reversed(sorted(sentences_being_shortened)):
                del self.knowledge[id]


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        unexplored_safes = self.safes - self.moves_made
        return unexplored_safes.pop() if len(unexplored_safes) else None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        unexplored = {(i, j) for i in range(self.height) 
            for j in range(self.width)} - self.moves_made - self.mines
        return unexplored.pop() if len(unexplored) else None
