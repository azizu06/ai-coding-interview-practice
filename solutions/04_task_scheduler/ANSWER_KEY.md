# 04 Task Scheduler: answer key

## The two bugs in `TaskGraph`

1. `add_dependency` records the dependents edge backwards. It does
   `self._dependents[task].add(depends_on)`, so `dependents_of("fetch")` comes back empty
   and `dependents_of("deploy")` lists deploy's own dependencies. Fix:
   `self._dependents[depends_on].add(task)`. `test_dependents_of` and
   `test_dependents_of_final_task` expose it, and `main.py` prints "unblocks" lists that
   mirror the "needs" lists.
2. `ready_tasks` forgets to exclude tasks that are already done. After fetch finishes,
   `ready_tasks({"fetch"})` returns `["compile", "fetch", "lint"]`. Fix: add
   `name not in done` to the condition. `test_ready_after_fetch` and
   `test_ready_when_everything_is_done` expose it; `main.py` shows fetch as ready again
   after it has run.

## Expected values for the `????` tests

See `expected.json`. Makespans: small 66, medium 227, large 395, huge 376, long chain
149953. The example order is fetch, compile, lint, package, test, deploy.

## Brute force

Order: repeat "ask the graph for every ready task, run the alphabetically first one" until
nothing is left. Each round scans every task, so that is O(V * (V + E)). Finish times:
sweep every task and relax `finish = duration + max(finish of dependencies)` until a full
sweep changes nothing, which is O(depth * (V + E)). It passes 2000 tasks in 0.2 s and is
killed at 3x the budget on 20000 tasks. See `brute_force_solver.py`.

## Optimization ladder

| Rung | Idea | Complexity | Passes | Breaks on |
| --- | --- | --- | --- | --- |
| 1 | Rescan all tasks each round; relax finish times until stable | O(V * (V + E)) | medium | large, huge, long |
| 2 | Kahn's algorithm: count unfinished dependencies per task, keep the zero-count tasks in a min-heap, decrement dependents as tasks pop. Finish times still by relaxation sweeps, or by a recursive memoized longest path | O((V + E) log V) for the order; relaxation is O(depth * (V + E)) | medium, large, huge (1.4 s of 2 s with relaxation) | long chain: depth equals V, so relaxation is 50000 sweeps over 50000 tasks; the recursive version hits Python's recursion limit instead |
| 3 | Kahn's order, then one pass over that order: every dependency of a task appears earlier, so its finish time is already known | O((V + E) log V) total, no recursion | everything (100000 tasks in 0.3 s, the chain in 0.1 s) | |

Rung 3 is the reference in `solver.py`. A cycle shows up as an order that is shorter than
the task count, which is what `has_cycle` checks.

## Good AI prompts

1. "The docstring defines dependency and dependent. Read add_dependency and tell me which
   map each line updates and whether the direction matches the definition." (Points at the
   vocabulary the bug violates.)
2. "I have a topological order from Kahn's algorithm. Explain why walking that order lets
   me compute each task's earliest finish in one pass without recursion, and what breaks
   if I recurse instead on a 50000 task chain." (Asks for the invariant and the failure.)
3. "Add a test where four tasks form a cycle plus one task hanging off it, and assert that
   has_cycle is True and execution_order raises." (Turns the edge case into a test.)

## Bad AI prompts

1. "Write a topological sort." (You will get a DFS with recursion, which blows the stack
   on the chain test, and it will ignore the alphabetical tie-break rule.)
2. "Why is dependents_of wrong?" without the docstring. (The agent cannot know which
   direction was intended.)
3. "Speed up finish_times" while still building the order with repeated scans. (The order
   is the quadratic part on large and huge; fixing the wrong stage first wastes minutes.)
