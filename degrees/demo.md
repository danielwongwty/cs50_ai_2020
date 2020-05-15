# Demo

A video demo is captured and uploaded to [youtube](https://youtu.be/fbku5PGWUMI).

1. Assume there's path between `source` and `target`, `shortest_path()` returns a list of `(movie_id, person_id)` tuples. Let's test with the **small** dataset.

    ```python
    import degrees

    degrees.load_data("small")

    p1 = degrees.person_id_for_name("Kevin Bacon")
    p2 = degrees.person_id_for_name("Sally Field")

    degrees.shortest_path(p1, p2)
    ```

    The above example returns `[('112384', '158'), ('109830', '398')]`. 

2. If there's no possible path between two actors, return `None`.

    ```python
    p3 = degrees.person_id_for_name("Emma Watson")

    degrees.shortest_path(p1, p3)
    ```

    You will get a `None` in the above example.

3. `shortest_path()` returns one of the multiple paths of minimum length from the source to the target. We test by querying the same example as the instruction against the **large** dataset: separation between *Emma Watson* and *Jennifer Lawrence*, which should not be more than 3 separations.
