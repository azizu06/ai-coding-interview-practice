# 06 Maze Solver: answer key

## The two bugs in `maze.py`

1. `is_open()` checks a door with `return ch in keys`. `ch` is the uppercase
   door letter and `keys` holds lowercase key letters, so no door ever opens.
   Fix: `return ch.lower() in keys`. Caught by `test_door_is_open_with_key`
   and `test_neighbors_through_door_with_key`.
2. `neighbors()` bounds-checks the column with `0 <= nc < self.cols - 1`, so
   the last column is never returned as a neighbor. Any maze whose route
   needs the right hand column looks unsolvable. Fix: `0 <= nc < self.cols`.
   Caught by `test_neighbors_in_last_column` (and the example maze, whose
   key `a` sits one cell left of the wall but the route to `G` runs down the
   last open column).

Filled-in `????` values: see `expected.json` in this folder.

## Brute force: depth-first search that revisits

`brute_force_solver.py` walks the maze depth first, keeping the best known
distance per `(cell, keys)` state and re-expanding a state whenever it finds
a shorter way in. It is correct, and on corridor-shaped mazes it is quick,
but on an open field the number of re-expansions explodes because depth
first order finds long routes first and then keeps improving them.

Cost: exponential in the worst case. Passes small (20x20) and medium
(30x30). Fails `test_large_maze_timed` (120x120, well over 12 s against a
1 s budget).

## Optimization ladder

### Rung 1: BFS over (cell, keys) states

The obvious fix: breadth first search, with a visited set keyed on
`(row, col, keys)`. Plain `(row, col)` is not enough, because you may need
to walk back through visited cells after picking up a key
(`test_must_backtrack_through_visited_cells` catches that mistake).

Cost: `O(cells * 2^K)` states. Passes small, medium and large. Fails
`test_huge_maze_timed`: 300x300 with six keys lying in the open means nearly
all 64 key combinations are reachable at every cell, about 4 million states,
around 3.6 s against a 1 s budget. See `state_bfs_solver.py`.

### Rung 2: compress to points of interest, then Dijkstra

Only a handful of cells matter: `S`, `G`, every key and every door. Run one
BFS from each of those points, stopping when it reaches another point, to
get pairwise walking distances that ignore key rules. Then run Dijkstra on
that tiny graph with states `(point, key mask)`: a door edge may be taken
only when the mask has its key, and arriving on a key sets its bit.

Cost: `P` grid BFS runs plus Dijkstra over `P * 2^K` states, where
`P = 2 + keys + doors` (14 on the huge maze). About 0.08 s on the huge maze.
Reference: `solver.py`.

Stopping the BFS at points of interest is what keeps it correct: a route
that walks through a key or a door is represented as two edges, so the mask
is updated or checked at the right moment.

## Timed test summary (measured on an Apple M5 Pro)

| test | size | budget | brute | state BFS | reference |
| --- | --- | --- | --- | --- | --- |
| small | 20x20, 1 key | 1.0 s | 0.00 s | 0.00 s | 0.00 s |
| medium | 30x30, 2 keys | 1.0 s | 0.01 s | 0.00 s | 0.00 s |
| large | 120x120, 3 keys | 1.0 s | > 12 s | 0.03 s | 0.01 s |
| huge | 300x300, 6 keys | 1.0 s | > 12 s | 3.6 s | 0.08 s |

## Good AI prompts

1. "Read `maze.py` and list every place a door or the grid boundary is
   handled. Which of those would make `test_neighbors_in_last_column` fail?"
2. "My BFS keys the visited set on `(row, col)`. Give me the smallest maze
   where that returns the wrong answer." (leads to the state BFS)
3. "The huge maze has six keys in the open, so `(cell, mask)` BFS explores
   about 4 million states. Sketch an approach whose cost depends on the
   number of keys and doors rather than the number of cells times 2^K."

## Bad AI prompts

1. "Fix the bugs in maze.py." (no test to anchor it; the agent may rewrite
   working code or change the neighbor order the tests depend on)
2. "Make the tests pass." (it will happily edit the tests or the budgets)
3. "Write the fastest maze solver possible." (you get A* or heuristics
   without a check that keys still work; the correctness tests come first)
