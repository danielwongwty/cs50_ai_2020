# Demo

This document demonstrate the functioning of methods implemented by me in
`shopping.py`, to make sure they're strictly following the specification. To
have a quick check please parse this file with `doctest`.

Let's import the methods first:

    >>> from shopping import *

-----

## Method Illustration

### `load_data(filename)`

This method parse the given .csv file and return its data as a tuple of 2
`list` (namely `evidence` and `labels`).

    >>> evidence, labels = load_data("shopping.csv")

`evidence` is a list of `list` object. Each `list` object should be of length
17 (for the case of "shopping.csv"). Every value in the `list` object is either
an `int` or a `float`.

    >>> isinstance(evidence, list)
    True
    >>> for element in evidence:
    ...     if (not isinstance(element, list) or    # each element is a `list`
    ...         len(element) != 17 or               # length of an element = 17
    ...         any(not isinstance(v, int) and 
    ...             not isinstance(v, float) 
    ...             for v in element
    ...             )                               # values are `int` / `float`
    ...         ):
    ...         raise Exception("Incorrect data format")

`labels` is a list of value of either 0 or 1.

    >>> isinstance(labels, list)
    True
    >>> for element in labels:
    ...     if not element in [0, 1]:
    ...         raise Exception("Incorrect data format")

The length of both `evidence` and `labels` are equal to the number of row of
the csv file, excluding the header row (which should be 12330 for
"shopping.py").

    >>> len(evidence) == len(labels) == 12330
    True
  
### `train_model(evidence, labels)`

Given a list of `evidence` lists and a list of `labels`, this method returns a
fitted `KNeighborsClassifier` trained on the data.

    >>> from sklearn.model_selection import train_test_split
    >>> from sklearn.neighbors import KNeighborsClassifier
    >>> X_train, X_test, y_train, y_test = train_test_split(
    ...     evidence, labels, test_size=TEST_SIZE
    ... )
    >>> model = train_model(X_train, y_train)
    >>> isinstance(model, KNeighborsClassifier)
    True
  
### `evaluate(labels, predictions)`

Given a list of `labels` and a list of `predictions`, return the tuple of 2
`float`: `sensitivity`, true-positive rate between 0 and 1, and `specificity`,
true-negative rate between 0 and 1.

    >>> predictions = model.predict(X_test)
    >>> sensitivity, specificity = evaluate(y_test, predictions)
    >>> 0.0 <= sensitivity <= 1.0
    True
    >>> 0.0 <= specificity <= 1.0
    True

-----

## Program Demo

Let's show the running of the program with the given data, "shopping.csv", for
4 times. We'll run the follow call in console:

    > python shopping.py shopping.csv

Please watch the screencast for the details.
