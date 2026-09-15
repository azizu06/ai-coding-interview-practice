# 05 Route Planner: answer key

## The two bugs in `RoadMap`

1. `add_road` only writes one direction. It does `self._roads[a][b] = minutes` and never
   `self._roads[b][a] = minutes`, so every road is one way even though the docstring says
   roads connect both stops. Fix: write both entries. `test_roads_are_two_way`,
   `test_neighbors_include_every_road` and `test_road_count_counts_each_road_once` all
   expose it. `road_count` divides the total link count by two, so with one-way roads it
   reports half the real number, which is the loudest signal. `main.py` also prints
   `direct downtown to airport: None` right under a road it just added.
2. `add_road` lets a later road overwrite an earlier one even when the later one is
   slower. The docstring says the faster time wins when the same pair is added again. Fix:
   read the current value first and only write when there is none or the new time is
   smaller. `test_faster_road_wins` exposes it, and `main.py` re-adds airport to downtown
   at 30 minutes and then prints 30 where it should print 20.

Both bugs hide in the same three lines, which is the point. The first one is visible from
any traversal; the second one only shows up when a pair of stops is given two roads, which
is exactly what the loaders do when a grid file lists a road from both ends.

## Expected values for the `????` tests

See `expected.json`. On the example map: airport to downtown 17, airport to beach 27,
airport to harbor 25, the three nearest to downtown are campus 5, harbor 8, beach 11.
Totals for the timed tests are 734 (medium), 1772 (large), 4965 (huge trips) and 4366
(huge nearest-five).

## Brute force

Dijkstra with a linear scan for the closest unsettled stop, rerun from scratch for every
query. That is O(V^2) per query. It answers the 900 stop map in 0.05 s and is killed at
three times the budget on the 10000 stop map, where the scan alone is 100 million
comparisons for ten trips. See `brute_force_solver.py`.

Breadth-first search is the other thing people reach for first, and it is simply wrong
here: it counts roads, not minutes, so on the example map it reports airport to downtown
as one hop and misses the 17 minute route through campus. The uncommented correctness
tests catch that before the timed tests ever run.

## Optimization ladder

| Rung | Idea | Complexity | Passes | Breaks on |
| --- | --- | --- | --- | --- |
| 1 | Dijkstra, scan every unsettled stop to find the closest | O(V^2) per query | medium (0.05 s of 1 s) | large: about 6.5 s against a 1 s budget |
| 2 | Same search with a binary heap, still exploring the whole map per query | O(E log V) per query | medium, large (0.09 s of 1 s) | both huge tests: 100 short trips take about 12 s against 2 s, and 200 nearest-five queries take about 23 s against 1 s |
| 3 | Stop as soon as the destination is settled (or as soon as k stops are settled), and read the adjacency table out of the `RoadMap` once instead of per visit | O(E' log V) where E' covers only the stops closer than the answer | everything: 0.08 s and 0.05 s on the huge map | |

Rung 2 is in `heap_solver.py` if you want to run the middle step yourself. Rung 3 is the
reference in `solver.py`.

The huge tests are what make rung 3 necessary, and they do it for two separate reasons.
The trips are at most fifteen rows and columns apart on a 300 by 300 grid, so a full
search settles 90000 stops to answer a question that only needs a few thousand. And
`neighbors()` builds a fresh sorted list every time it is called, so a full search per
query pays for 90000 sorts, a hundred times over. Caching the adjacency table without the
early exit, or the early exit without the cache, each gets you part of the way. You need
both to clear 1 second on the nearest-five test.

`nearest_stops` is the easier half to get wrong quickly. Settling the whole map and then
sorting is O(V log V) per query no matter how good the search is. Dijkstra settles stops
in increasing distance order, so you can stop the moment k of them are out, and the heap
already breaks ties by name because it holds `(minutes, stop)` tuples.

## Good AI prompts

1. "The RoadMap docstring says roads are two way and that the faster time wins on a repeat
   add. Walk me through add_road line by line and tell me which of those two sentences the
   code actually implements." (Names the contract, asks for a comparison against it,
   instead of asking where the bug is.)
2. "Give me a concise list of options for answering 100 shortest-path queries on a 90000
   stop grid where the two stops are always within fifteen blocks of each other. Do not
   write code yet." (The "within fifteen blocks" detail is the whole problem, and asking
   for a list rather than an answer surfaces early exit, bidirectional search and A* so
   you can pick.)
3. "Time how long `road_map.neighbors(stop)` takes for 90000 calls and compare it against
   one full Dijkstra run on the same map." (Turns a hunch about the sorted list into a
   measurement.)

## Bad AI prompts

1. "Write a shortest path function." (Half the time you get BFS, which ignores the
   minutes, and the correctness tests fail in a way that looks like a bug in your map.)
2. "Make it faster." (With the brute force in context the model tunes the linear scan
   rather than replacing it. Clear the chat and describe the shape of the queries instead.)
3. "Is this O(V log V)?" (Leading. Ask "what is the time complexity per query if V is the
   number of stops and E is the number of roads" and check the answer against your own.)
