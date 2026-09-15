# 02 Spell Checker

Difficulty: Easy

## Problem

You are given a dictionary of known words and a stream of typed words. For each typed word,
suggest every dictionary word that is within a small number of edits. An edit is inserting
one letter, deleting one letter, or replacing one letter.

The `Dictionary` class in `src/dictionary.py` normalizes words (case, surrounding
whitespace, surrounding punctuation) and answers "is this a known word". The `Solver` class
in `src/solver.py` produces the suggestions.

## Example

Dictionary:

```
apple, apply, ample, maple, grape, graph, great, treat, tread, bread
```

Queries and suggestions within one edit:

```
grapf   -> grape, graph
bred    -> bread
Apple!  -> ample, apple, apply     (the query is normalized first; apple is 0 edits away)
zzzzz   -> (nothing)
```

Within two edits, `grate` gives `grape, graph, great`.

## Files

```
data/dictionary_small.txt         100 words
data/dictionary_medium.txt        5000 words
data/dictionary_large.txt         50000 words
data/queries_medium.txt           20 queries, one edit away
data/queries_large.txt            300 queries, one edit away
data/queries_huge.txt             3000 queries, one edit away
data/queries_distance_two.txt     200 queries, two edits away
data/gen_data.py                  the script that produced the files above
src/main.py                       runnable demo
src/dictionary.py                 the Dictionary class (read this first)
src/word_files.py                 loaders for the data files
src/solver.py                     the Solver stub you complete
src/test_dictionary.py            unit tests for Dictionary
src/test_solver.py                unit tests for Solver, correctness first, then timed
```

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `Dictionary` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `suggest()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.
