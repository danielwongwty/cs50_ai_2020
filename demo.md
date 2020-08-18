# Demo

This file is written to demonstrate some tests on methods implemented by us in  
this project, in order to make sure they are implemented as required in the  
specifications. You may try to call `doctest` module for a fast check.

Let's import all involved modules first:

    >>> from crossword import *
    >>> from generate import *

-----

## `CrosswordCreator.enforce_node_consistency()`

This method updates `self.domains` such that each variable is node-consistent.  
In other words, remove any word in the domain which is not the same length as  
specified in the `self.crossword.variables`. Let's check it.

Initial some variables first:

    >>> structure = "data/structure1.txt"
    >>> words = "data/words1.txt"
    >>> crossword = Crossword(structure, words)
    >>> creator = CrosswordCreator(crossword)

Before running the method:

    >>> any(len(word) != var.length
    ...     for var in creator.crossword.variables
    ...     for word in creator.domains[var])
    True

Let's run the method and check it again:

    >>> creator.enforce_node_consistency()
    >>> any(len(word) != var.length
    ...     for var in creator.crossword.variables
    ...     for word in creator.domains[var])
    False

## `CrosswordCreator.revise(x, y)`

This method updates `self.domains[x]` such that `x` is arc-consistent with  
another variable `y`, which is to remove any word in `self.domains[x]` which  
does not have a corresponding possible value in `self.domains[y]` such that  
it satisfy the overlapping constraint. Return `True` if any invalid word is  
found; otherwise return `False`.

Let's test the following overlapping variables:

    >>> x = Variable(4, 4, 'across', 5)
    >>> y = Variable(1, 7, 'down', 7)
    >>> i, j = creator.crossword.overlaps[x, y]

Now let's test for their arc-consistency:

    >>> any(not any(len(word_x) > i and len(word_y) > j and 
    ...             word_x[i] == word_y[j] 
    ...             for word_y in creator.domains[y]) 
    ...     for word_x in creator.domains[x])
    True

And we call the method to enforce arc-consistency:

    >>> domain_size_x = len(creator.domains[x])
    >>> domain_size_y = len(creator.domains[y])
    >>> creator.revise(x, y)
    True

Check its arc-consistency again:

    >>> any(not any(len(word_x) > i and len(word_y) > j and 
    ...             word_x[i] == word_y[j] 
    ...             for word_y in creator.domains[y]) 
    ...     for word_x in creator.domains[x])
    False

Check if something is removed from domain of `x` but not from that of `y`:

    >>> len(creator.domains[x]) < domain_size_x
    True
    >>> len(creator.domains[y]) == domain_size_y
    True

Which shows that its arc-consistent now. And we try to call the method again:

    >>> creator.revise(x, y)
    False

Returning `False` means that no invalid word could be found in its domain now.

## `CrosswordCreator.ac3(arcs=None)`

It runs `CrosswordCreator.revise()` at all specified arcs (or all found arcs  
if `arcs` is not specified) to make sure that those arcs are consistent. If  
any domain is found empty during the process, `False` would be returned;  
otherwise, `True` is returned after finish running `revise()` at all those  
arcs.

Let's check the original domain size, then run `ac3()` and see if they are  
smaller than or the same as before.

    >>> domain_sizes = {v: len(creator.domains[v]) for v in creator.domains}

Now, run `ac3()` and compare:

    >>> creator.ac3()
    True
    >>> all(len(creator.domains[v]) <= domain_sizes[v] 
    ...     for v in creator.domains)
    True

## `CrosswordCreator.assignment_complete(assignment)`

Check if the specified dict, `assignment`, has been filled with all variables  
mapped with `string`, regardless of what those values are. Let's check it out:

    >>> assignment = {v: "" for v in creator.crossword.variables}
    >>> creator.assignment_complete(assignment)
    True

And if there's any variable missing, it should returns `False`:

    >>> _ = assignment.popitem()
    >>> creator.assignment_complete(assignment)
    False

## `CrosswordCreator.consistent(assignment)`

`assignment` is a dict in which the keys are `Variable` objects, and values  
are strings of words which those variables will take on.

This method returns `True` if `assignment` satisfies the followings:

1. all values are distinct
2. every value is the correct length
3. there are no conflicts between neighboring variables

Let's test on 1 satisfying case and 3 controls:

    >>> creator.consistent({                # Satisfying case
    ...     Variable(1, 7, 'down', 7):      "minimax",
    ...     Variable(2, 1, 'across', 12):   "intelligence"
    ... })
    True

    >>> creator.consistent({                # Control of distinct value check
    ...     Variable(1, 7, 'down', 7):      "minimax",
    ...     Variable(1, 12, 'down', 7):     "minimax"
    ... })
    False

    >>> creator.consistent({                # Control of correct length check
    ...     Variable(1, 7, 'down', 7):      "minimax",
    ...     Variable(1, 12, 'down', 7):     "search"
    ... })
    False

    >>> creator.consistent({                # Control of conflict check
    ...     Variable(1, 7, 'down', 7):      "resolve",
    ...     Variable(2, 1, 'across', 12):   "intelligence",
    ... })
    False

## `CrosswordCreator.order_domain_values(var, assignment)`

return a list of all of the values in the domain of var, ordered according to  
the least-constraining values heuristic.

To clearly check and manipulate its functionality, I've made another method,  
`CrosswordCreator.get_affected_variable_count(var, assignment)`, which is to  
calculate the count of affected variables for each word in the domain of `var`,  
and return as a dict.

We use this case to test it (data/my_structure.txt):

    ########  
    #_###_##  
    #_____##  
    #_#_#_##  
    #______#  
    #_#_#_##  
    #______#  
    ########  

Let's initialize the value and enforce the node- and arc- consistency:

    >>> structure = "data/my_structure.txt"
    >>> words = "data/words2.txt"
    >>> crossword = Crossword(structure, words)
    >>> creator = CrosswordCreator(crossword)

    >>> creator.enforce_node_consistency()
    >>> creator.ac3()
    True

We query the values of the heuristic method provided:

    >>> var = Variable(1, 1, 'down', 6)
    >>> heuristic = creator.get_affected_variable_count(var, {})

As the heuristic info is quite large, let's see the heuristic values we've got:

    >>> sorted(set(heuristic.values()))
    [0, 1, 2]

Let's check if `CrosswordCreator.order_domain_values(var, assignment)` follows  
the ascending order of our heuristic values:

    >>> current_heuristic_value = -1
    >>> for word in creator.order_domain_values(var, {}):
    ...     if heuristic[word] < current_heuristic_value:
    ...         raise Exception("Incorrect sorting")
    ...     else:
    ...         current_heuristic_value = heuristic[word]

No error occurs, meaning that the returned list follows the order of our  
heuristic values.

## `CrosswordCreator.select_unassigned_variable(assignment)`

It returns a single variable in the crossword puzzle that is not yet assigned  
by `assignment`. The variable is chosen with the following heuristic:

1. Has the least number of choices in the domain among all unassigned variables
2. If there's a tie for point 1 between 2 variables, choose the one with more  
   neighbor

For the convenience of comparing, another method,  
`CrosswordCreator.get_domain_size_and_neg_neigbor_count()` is written. To find  
the best value, just find the least heuristic value among all variables.

Let's print all the variables and their heuristic values first. Here we would  
try to use the above utility method for sorting.

    >>> variables = sorted(creator.crossword.variables,
    ...                    key=creator.get_domain_size_and_neg_neigbor_count)
    >>> for var in variables:
    ...     print(f"var: {repr(var):<30} "
    ...           f"domain_size: {len(creator.domains[var]):<6} "
    ...           f"neighbor_count: {len(creator.crossword.neighbors(var))}")
    ... 
    var: Variable(6, 1, 'across', 6)    domain_size: 382    neighbor_count: 3
    var: Variable(1, 5, 'down', 6)      domain_size: 433    neighbor_count: 3
    var: Variable(2, 1, 'across', 5)    domain_size: 457    neighbor_count: 3
    var: Variable(2, 3, 'down', 5)      domain_size: 478    neighbor_count: 3
    var: Variable(1, 1, 'down', 6)      domain_size: 481    neighbor_count: 3
    var: Variable(4, 1, 'across', 6)    domain_size: 484    neighbor_count: 3

And let's try several calls on `CrosswordCreator.select_unassigned_variable()`:

    >>> creator.select_unassigned_variable({}) 
    Variable(6, 1, 'across', 6)
    >>> creator.select_unassigned_variable({
    ...     Variable(6, 1, 'across', 6): "", 
    ...     Variable(2, 1, 'across', 5): ""
    ... }) 
    Variable(1, 5, 'down', 6)

## `CrosswordCreator.backtrack(assignment)`

The backtrack function should accept a partial assignment assignment as input  
and, using backtracking search, return a complete satisfactory assignment of  
variables to values if it is possible to do so.

As it's rather difficult to test the behavior by simple case, we'll check its  
performance by solving different crossword puzzles directly.

According to the requirement, we have to run the following calls:

    > python generate.py data/structure0.txt data/words0.txt output.png
    > python generate.py data/structure0.txt data/words1.txt output.png
    > python generate.py data/structure1.txt data/words1.txt output.png
    > python generate.py data/structure2.txt data/words2.txt output.png

The above calls will be demonstrated in the screencast.
