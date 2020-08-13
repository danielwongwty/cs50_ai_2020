# Demo

Here we demonstrate the calling of some functions to make sure they are  
implemented as required in the specifications. You may try to call `doctest`  
module for a fast check.

Let's import the `heredity` module first before testing them.

    >>> from heredity import *

-----

We have implemented 3 functions in this project:

- `joint_probability(people, one_gene, two_genes, have_trait)`
- `update(probabilities, one_gene, two_genes, have_trait, p)`
- `normalize(probabilities)`

As most of the specifications are encapsulated within the methods themselves  
and it's hard to reveal by running simple case, here we try to run the  
example given in the specifications.

    >>> people = {
    ...   'Harry': {'name': 'Harry', 'mother': 'Lily', 
    ...             'father': 'James', 'trait': None},
    ...   'James': {'name': 'James', 'mother': None, 
    ...             'father': None, 'trait': True},     
    ...   'Lily': {'name': 'Lily', 'mother': None, 
    ...            'father': None, 'trait': False}       
    ... }
    >>> joint_probability(people, {"Harry"}, {"James"}, {"James"})
    0.0026643247488

The value we get is the same as that in the example.
