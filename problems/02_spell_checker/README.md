# 02 Spell Checker

*For every typed word, name every dictionary word within a small number of edits.*

|  |  |
| --- | --- |
| **Difficulty** | Easy |
| **Topics** | Edit distance, indexing |
| **Files you edit** | `src/dictionary.py`, `src/solver.py` |
| **Timed budget** | 4 timed tests, 1.0 s each |
| **Suggested time** | 50 min |

## The problem

You are given a dictionary of known words and a stream of typed words. For each typed word,
suggest every dictionary word that is within a small number of edits. An edit is inserting
one letter, deleting one letter, or replacing one letter.

The `Dictionary` class in `src/dictionary.py` normalizes words (case, surrounding
whitespace, surrounding punctuation) and answers "is this a known word". The `Solver` class
in `src/solver.py` produces the suggestions.

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

## The codebase

| File | What it holds |
| --- | --- |
| `data/dictionary_small.txt` | 100 words |
| `data/dictionary_medium.txt` | 5000 words |
| `data/dictionary_large.txt` | 50000 words |
| `data/queries_medium.txt` | 20 queries, one edit away |
| `data/queries_large.txt` | 300 queries, one edit away |
| `data/queries_huge.txt` | 3000 queries, one edit away |
| `data/queries_distance_two.txt` | 200 queries, two edits away |
| `data/gen_data.py` | the script that produced the files above |
| `src/main.py` | runnable demo |
| `src/dictionary.py` | the Dictionary class, read this first |
| `src/word_files.py` | loaders for the data files |
| `src/solver.py` | the Solver stub you complete |
| `src/test_dictionary.py` | unit tests for Dictionary |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `Dictionary` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `suggest()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/02_spell_checker/src/main.py
python -m unittest discover -s problems/02_spell_checker/src -v
```

From inside `problems/02_spell_checker/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_dictionary -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

## Hints for using your AI well

- Good prompt: paste the `Dictionary` docstring next to `normalize`, then ask for a step by
  step trace of `normalize('Hello! ')` against the order the docstring promises.
- Watch for: a second normalizer written inside the solver that disagrees with `Dictionary`,
  and a suggestion to reach for a trie, which is a lot of code for a 50 minute slot and
  still loses to a deletion index here.
- Test to tighten: add a case proving a word two substitutions away is found, not only one
  edit away.

---

Spoilers ahead: [`../../solutions/02_spell_checker/ANSWER_KEY.md`](../../solutions/02_spell_checker/ANSWER_KEY.md)
names both bugs, the whole optimization ladder and the expected values. Do not open it until
your timer is done.
