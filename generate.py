import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            self.domains[var] -= {word for word in self.domains[var]
                                  if len(word) != var.length}

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is None:
            return False        # No revision required
        i, j = self.crossword.overlaps[x, y]
        invalid_words = {word_x for word_x in self.domains[x] 
                         if not any(word_x[i] == word_y[j] 
                                    for word_y in self.domains[y])
                         }
        self.domains[x] -= invalid_words
        return len(invalid_words) > 0

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        arcs = set(self.crossword.overlaps if arcs is None else arcs)
        frontier = arcs.copy()
        while len(frontier):
            x, y = frontier.pop()
            if self.revise(x, y):                   # if anything is removed
                if len(self.domains[x]) == 0:       # if domain[x] is empty
                    return False                    # there's no valid solution
                # Otherwise, add its neighbors and check again
                frontier |= (self.crossword.neighbors(x) & arcs) - set((x, y))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(v in assignment and isinstance(assignment[v], str)
                   for v in self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if the values are distinct
        if len(assignment.keys()) != len(set(assignment.values())):
            return False

        # Check if the values have correct length
        for v in assignment:
            if (not isinstance(assignment[v], str) or 
                len(assignment[v]) != v.length):
                return False

        # Check if there's no conflict between neghiboring variables
        for v1 in assignment:
            for v2 in self.crossword.neighbors(v1):
                if v2 in assignment:
                    i, j = self.crossword.overlaps[v1, v2]
                    if assignment[v1][i] != assignment[v2][j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        num_affected_domain = self.get_affected_variable_count(var, assignment)
        rtn = sorted(self.domains[var], key=lambda w: num_affected_domain[w])
        return rtn

    def get_affected_variable_count(self, var, assignment):
        """
        Given a Variable `var` and a dict of assigned values `assignment`,
        return a dict of domain values of `var` mapped with total number of
        affected neighbors. neighbors with values assigned in `assignment` are
        not treated as affected neighbors. This is used as the
        least-constraining value heuristic for another method
        `order_domain_values()`.
        """
        neighbors = self.crossword.neighbors(var) - set(assignment)
        # Number of affected neighbors for each word
        return {
            word: sum(int(word in self.domains[n]) for n in neighbors)
            for word in self.domains[var]
        }

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        rtn = None
        heuristic_value = None
        for var in self.crossword.variables - set(assignment):
            h = self.get_domain_size_and_neg_neigbor_count(var)
            if rtn is None or h < heuristic_value:
                rtn = var
                heuristic_value = h
        return rtn

    def get_domain_size_and_neg_neigbor_count(self, var):
        """
        Return a tuple of 2 values, in which the 1st one is the size of the
        domain of the given `var`, and the 2nd one is the negative of the total
        number of neighbor of the given `var`. This method is used as the 
        heuristic for `select_unassigned_variable()`.

        Note: the negation for the 2nd value is for the convenience of
                comparing, so that we can easily find the best one by getting
                the least value of this method output among all variables.
        """
        return len(self.domains[var]), -len(self.crossword.neighbors(var))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
                # Save the domain to run inferences (ac3)
                inferred_domains = {
                    d: self.domains[d].copy()
                    for d in {var} | self.crossword.neighbors(var)
                }
                self.domains[var] = {word}
                if self.ac3([(n, var) for n in self.crossword.neighbors(var)]):
                    rtn = self.backtrack(assignment)
                    if rtn is not None:
                        return rtn
                # Restore the domains
                for d in inferred_domains:
                    self.domains[d] = inferred_domains[d]
            del assignment[var]
        return None
        


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
