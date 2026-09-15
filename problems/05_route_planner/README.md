# 05 Route Planner

*Find the quickest trip between two transit stops, and the k stops nearest to one.*

|  |  |
| --- | --- |
| **Difficulty** | Medium |
| **Topics** | Weighted graphs, Dijkstra |
| **Files you edit** | `src/road_map.py`, `src/solver.py` |
| **Timed budget** | 4 timed tests, 1.0 s to 2.0 s each |
| **Suggested time** | 50 min |

## The problem

A transit map has stops joined by two-way roads, each road labelled with a travel time in
whole minutes. Given two stops, find the fewest minutes it takes to get from one to the
other. Then, given one stop, find the `k` stops that are closest to it by travel time.

The `RoadMap` class in `src/road_map.py` stores the stops and the roads. The `Solver`
class in `src/solver.py` answers the two questions.

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

Maps are grids. The stop `r12c30` sits in row 12, column 30, and roads join it to its
horizontal and vertical neighbours.

Every map loader in `src/map_data.py` hands back a pair. The first half is a list of stop
names and the second is a list of `(a, b, minutes)` roads.

## The codebase

| File | What it holds |
| --- | --- |
| `data/map_small.txt` | 4 by 5 grid, 20 stops |
| `data/map_medium.txt` | 30 by 30 grid, 900 stops |
| `data/map_large.txt` | 100 by 100 grid, 10000 stops |
| `data/gen_data.py` | the script that produced the files above |
| `src/main.py` | runnable demo |
| `src/road_map.py` | the RoadMap class, read this first |
| `src/map_data.py` | loaders, plus an in-memory 300 by 300 grid and the query sets |
| `src/solver.py` | the Solver stub you complete |
| `src/test_road_map.py` | unit tests for RoadMap |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `RoadMap` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `shortest_time()` and `nearest_stops()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/05_route_planner/src/main.py
python -m unittest discover -s problems/05_route_planner/src -v
```

From inside `problems/05_route_planner/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_road_map -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

## Hints for using your AI well

- Good prompt: ask for a concise list of options for 100 trips on a 90000 stop grid where
  the two stops are always within fifteen blocks of each other, and say not to write code
  yet.
- Watch for: a breadth first search, which counts roads rather than minutes and calls
  airport to downtown one hop instead of 17 minutes.
- Test to tighten: add the same pair of stops twice with two different travel times and
  assert the faster road is the one that survives.

---

Spoilers ahead: [`../../solutions/05_route_planner/ANSWER_KEY.md`](../../solutions/05_route_planner/ANSWER_KEY.md)
names both bugs, the whole optimization ladder and the expected values. Do not open it until
your timer is done.
