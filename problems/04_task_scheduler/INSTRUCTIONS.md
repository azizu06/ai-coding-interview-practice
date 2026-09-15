# 04 Task Scheduler

Difficulty: Medium

## Problem

A build system has tasks with durations and dependencies. Produce an order in which the
tasks can run, and for each task the earliest moment it can finish when there are
unlimited workers. Report a cycle when the dependencies make the job impossible.

The `TaskGraph` class in `src/task_graph.py` stores tasks and dependencies. The `Solver`
class in `src/solver.py` computes the order, the finish times and the cycle check.

## Example

Tasks and durations:

```
fetch 2, compile 5, lint 1, test 4, package 2, deploy 3
```

Dependencies (task needs dependency):

```
compile needs fetch
lint needs fetch
test needs compile
package needs compile, lint
deploy needs test, package
```

Execution order (when several tasks are ready, the alphabetically smallest goes first):

```
fetch, compile, lint, package, test, deploy
```

Earliest finish times with unlimited workers:

```
fetch 2, compile 7, lint 3, package 9, test 11, deploy 14
```

## Files

```
data/tasks_small.txt      12 tasks
data/tasks_medium.txt     2000 tasks, about 3000 dependencies
data/gen_data.py          the script that produced the files above
src/main.py               runnable demo
src/task_graph.py         the TaskGraph class (read this first)
src/task_data.py          loaders, plus in-memory generators for 20000, 100000 and a 50000 task chain
src/solver.py             the Solver stub you complete
src/test_task_graph.py    unit tests for TaskGraph
src/test_solver.py        unit tests for Solver, correctness first, then timed
```

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `TaskGraph` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `execution_order()`, `finish_times()` and `has_cycle()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.
