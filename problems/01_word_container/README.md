# 01 Word Container

*Find every word in a list that hides another word from the same list inside it.*

|  |  |
| --- | --- |
| **Difficulty** | Medium |
| **Topics** | Strings, sets, tries |
| **Files you edit** | `src/word_list.py`, `src/solver.py` |
| **Timed budget** | 4 timed tests, 0.5 s to 1.0 s each |
| **Suggested time** | 50 min |

## The problem

You are given a list of words. A word is a "container" when some other word from the same
list appears inside it as a substring. Find every container word.

The `WordList` class in `src/word_list.py` cleans the raw input: it drops anything that is
not made of lowercase letters, drops repeats, and enforces a maximum length. The `Solver`
class in `src/solver.py` is where the search goes.

Input words:

```
cat, concatenate, dog, hotdog, sun, sunny, ate, plate, ten
```

Output, sorted:

```
concatenate   contains cat, ate, ten
hotdog        contains dog
plate         contains ate
sunny         contains sun
```

A word never counts as its own container. Words that appear twice in the input are treated
as one word.

## The codebase

| File | What it holds |
| --- | --- |
| `data/words_small.txt` | 20 words |
| `data/words_medium.txt` | 500 words |
| `data/words_large.txt` | 10000 words |
| `data/words_huge.txt` | 25000 words |
| `data/words_long.txt` | 30 words, most of them over 1500 letters long |
| `data/gen_data.py` | the script that produced the files above |
| `src/main.py` | runnable demo |
| `src/word_list.py` | the WordList class, read this first |
| `src/words.py` | loaders for the data files |
| `src/solver.py` | the Solver stub you complete |
| `src/test_word_list.py` | unit tests for WordList |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `WordList` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `find_container_words()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/01_word_container/src/main.py
python -m unittest discover -s problems/01_word_container/src -v
```

From inside `problems/01_word_container/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_word_list -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

## Hints for using your AI well

- Good prompt: ask your agent to write out the validation rules `WordList` actually enforces,
  then hold that list against what the tests expect, instead of asking where the bugs are.
- Watch for: a containment check that counts a word as containing itself, and a solution
  built on the set of all substrings, which is quick on 25000 short words and falls over on
  the 1500 letter words in `words_long.txt`.
- Test to tighten: feed the same word in twice and assert it still does not come back as its
  own container.

---

Spoilers ahead: [`../../solutions/01_word_container/ANSWER_KEY.md`](../../solutions/01_word_container/ANSWER_KEY.md)
names both bugs, the whole optimization ladder and the expected values. Do not open it until
your timer is done.
