# 01 Word Container

Difficulty: Medium

## Problem

You are given a list of words. A word is a "container" when some other word from the same
list appears inside it as a substring. Find every container word.

The `WordList` class in `src/word_list.py` cleans the raw input: it drops anything that is
not made of lowercase letters, drops repeats, and enforces a maximum length. The `Solver`
class in `src/solver.py` is where the search goes.

## Example

Input words:

```
cat, concatenate, dog, hotdog, sun, sunny, ate, plate, ten
```

Output (sorted):

```
concatenate   contains cat, ate, ten
hotdog        contains dog
plate         contains ate
sunny         contains sun
```

A word never counts as its own container. Words that appear twice in the input are treated
as one word.

## Files

```
data/words_small.txt     20 words
data/words_medium.txt    500 words
data/words_large.txt     10000 words
data/words_huge.txt      25000 words
data/words_long.txt      30 words, most of them over 1500 letters long
data/gen_data.py         the script that produced the files above
src/main.py              runnable demo
src/word_list.py         the WordList class (read this first)
src/words.py             loaders for the data files
src/solver.py            the Solver stub you complete
src/test_word_list.py    unit tests for WordList
src/test_solver.py       unit tests for Solver, correctness first, then timed
```

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `WordList` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `find_container_words()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.
