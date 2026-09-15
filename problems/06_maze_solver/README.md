# 06 Maze Solver

*Walk a grid maze of walls, keys and doors in as few steps as possible.*

|  |  |
| --- | --- |
| **Difficulty** | Medium |
| **Topics** | Grid BFS, state search |
| **Files you edit** | `src/maze.py`, `src/solver.py` |
| **Timed budget** | 4 timed tests, 1.0 s each |
| **Suggested time** | 50 min |

## The problem

You are given a small codebase that models a grid maze with walls, keys and doors. A `Maze`
class already parses the grid and answers questions like "which cells can I step to from
here". Your job is to find the shortest walk from the start `S` to the goal `G`.

```
#   wall, never passable
.   open floor
S   start
G   goal (the exit)
a-f a key lying on the floor; stepping onto the cell picks it up
A-F a door; you may step onto it only while carrying the matching key
```

You move one cell at a time: up, down, left or right. A picked-up key is kept forever, so
every door of that letter stays open once you hold the key. You may walk over the same cell
as many times as you like.

```
#########
#S..#..a#
#.#.#.#.#
#.#...#.#
#.#####.#
#...A..G#
#########
```

The shortest walk from `S` to `G` is 14 steps: down the middle passage to pick up `a`, then
down the right hand column to `G`. Door `A` is never needed here, and the direct route
through it is walled off anyway.

`Solver(maze).shortest_path()` should return `14` for this maze, and `-1` for a maze where
the goal cannot be reached.

## The codebase

| File | What it holds |
| --- | --- |
| `data/maze_small.txt` | 20 by 20 grid, 1 key |
| `data/maze_medium.txt` | 30 by 30 grid, 2 keys |
| `data/maze_large.txt` | 120 by 120 grid, 3 keys |
| `data/maze_huge.txt` | 300 by 300 grid, 6 keys |
| `data/gen_data.py` | the script that regenerates the data files |
| `src/main.py` | runnable demo |
| `src/maze.py` | the Maze class, read this first |
| `src/mazes.py` | loaders for the data files |
| `src/solver.py` | the Solver stub you complete |
| `src/test_maze.py` | unit tests for Maze |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `Maze` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `shortest_path()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/06_maze_solver/src/main.py
python -m unittest discover -s problems/06_maze_solver/src -v
```

From inside `problems/06_maze_solver/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_maze -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

## Hints for using your AI well

- Good prompt: ask for the smallest maze where keying the visited set on `(row, col)` alone
  returns the wrong answer.
- Watch for: a visited set keyed on the cell rather than on the cell plus the keys held, and
  a door check that compares an uppercase door letter against lowercase keys.
- Test to tighten: build a maze whose only route runs through a door whose key is sealed
  behind walls, and assert the answer is `-1`.

---

Spoilers ahead: [`../../solutions/06_maze_solver/ANSWER_KEY.md`](../../solutions/06_maze_solver/ANSWER_KEY.md)
names both bugs, the whole optimization ladder and the expected values. Do not open it until
your timer is done.
