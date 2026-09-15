# 06 Maze Solver (Medium)

You are given a small codebase that models a grid maze with walls, keys and
doors. A `Maze` class already parses the grid and answers questions like
"which cells can I step to from here". Your job is to find the shortest walk
from the start `S` to the goal `G`.

## The rules of the maze

```
#   wall, never passable
.   open floor
S   start
G   goal (the exit)
a-f a key lying on the floor; stepping onto the cell picks it up
A-F a door; you may step onto it only while carrying the matching key
```

You move one cell at a time: up, down, left or right. A picked-up key is
kept forever, so every door of that letter stays open once you hold the key.
You may walk over the same cell as many times as you like.

## Example

```
#########
#S..#..a#
#.#.#.#.#
#.#...#.#
#.#####.#
#...A..G#
#########
```

The shortest walk from `S` to `G` is 14 steps: down the middle passage to
pick up `a`, then down the right hand column to `G`. Door `A` is never
needed here, but the direct route through it is walled off anyway.

`Solver(maze).shortest_path()` should return `14` for this maze, and `-1`
for a maze where the goal cannot be reached.

## Layout

```
src/
  maze.py        the Maze class (read this first)
  mazes.py       loaders for the data files
  main.py        runnable demo
  solver.py      the class you will implement
  test_maze.py   unit tests for Maze
  test_solver.py unit tests and timed tests for Solver
data/
  maze_small.txt, maze_medium.txt, maze_large.txt, maze_huge.txt
  gen_data.py    regenerates the data files
```

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `Maze` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `shortest_path()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as
you would in the real interview. Start a 50 minute timer.
