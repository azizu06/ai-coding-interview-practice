# 05 Route Planner

Difficulty: Medium

## Problem

A transit map has stops joined by two-way roads, each road labelled with a travel time in
whole minutes. Given two stops, find the fewest minutes it takes to get from one to the
other. Then, given one stop, find the `k` stops that are closest to it by travel time.

The `RoadMap` class in `src/road_map.py` stores the stops and the roads. The `Solver`
class in `src/solver.py` answers the two questions.

## Example

Six stops. `island` has no roads, so nothing reaches it.

```
airport  - downtown  20
airport  - campus    12
campus   - downtown   5
downtown - harbor      8
campus   - beach      15
harbor   - beach       3
```

Shortest times:

```
airport -> downtown   17   (through campus, the direct road takes 20)
airport -> beach      27   (airport, campus, beach)
airport -> harbor     25   (airport, campus, downtown, harbor)
island  -> beach      None
harbor  -> harbor       0
```

The three stops nearest to `downtown`:

```
campus 5, harbor 8, beach 11
```

## Files

```
data/map_small.txt     4 by 5 grid, 20 stops
data/map_medium.txt    30 by 30 grid, 900 stops
data/map_large.txt     100 by 100 grid, 10000 stops
data/gen_data.py       the script that produced the files above
src/main.py            runnable demo
src/road_map.py        the RoadMap class (read this first)
src/map_data.py        loaders, plus an in-memory 300 by 300 grid and the query sets
src/solver.py          the Solver stub you complete
src/test_road_map.py   unit tests for RoadMap
src/test_solver.py     unit tests for Solver, correctness first, then timed
```

Maps are grids. The stop `r12c30` sits in row 12, column 30, and roads join it to its
horizontal and vertical neighbours.

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `RoadMap` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `shortest_time()` and `nearest_stops()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.
