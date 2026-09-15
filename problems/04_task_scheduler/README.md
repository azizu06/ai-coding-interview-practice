# 04 Task Scheduler

*Order a build graph, report the earliest finish time of every task, and catch cycles.*

|  |  |
| --- | --- |
| **Difficulty** | Medium |
| **Topics** | Graphs, topological order |
| **Files you edit** | `src/task_graph.py`, `src/solver.py` |
| **Timed budget** | 4 timed tests, 1.0 s to 2.0 s each |
| **Suggested time** | 50 min |

## The problem

A build system has tasks with durations and dependencies. Produce an order in which the
tasks can run, and for each task the earliest moment it can finish when there are
unlimited workers. Report a cycle when the dependencies make the job impossible.

The `TaskGraph` class in `src/task_graph.py` stores tasks and dependencies. The `Solver`
class in `src/solver.py` computes the order, the finish times and the cycle check.

Tasks and durations:

```
fetch 2, compile 5, lint 1, test 4, package 2, deploy 3
```

Dependencies, where a task needs its dependency:

```
compile needs fetch
lint needs fetch
test needs compile
package needs compile, lint
deploy needs test, package
```

Execution order, where the alphabetically smallest of the ready tasks goes first:

```
fetch, compile, lint, package, test, deploy
```

Earliest finish times with unlimited workers:

```
fetch 2, compile 7, lint 3, package 9, test 11, deploy 14
```

## The codebase

| File | What it holds |
| --- | --- |
| `data/tasks_small.txt` | 12 tasks |
| `data/tasks_medium.txt` | 2000 tasks, about 3000 dependencies |
| `data/gen_data.py` | the script that produced the files above |
| `src/main.py` | runnable demo |
| `src/task_graph.py` | the TaskGraph class, read this first |
| `src/task_data.py` | loaders, plus in-memory generators for 20000, 100000 and a 50000 task chain |
| `src/solver.py` | the Solver stub you complete |
| `src/test_task_graph.py` | unit tests for TaskGraph |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `TaskGraph` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `execution_order()`, `finish_times()` and `has_cycle()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/04_task_scheduler/src/main.py
python -m unittest discover -s problems/04_task_scheduler/src -v
```

From inside `problems/04_task_scheduler/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_task_graph -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

## Hints for using your AI well

- Good prompt: give it the docstring definitions of dependency and dependent, then ask which
  map each line of `add_dependency` updates and whether the direction matches.
- Watch for: ask for a topological sort and you tend to get a recursive depth first search,
  which blows Python's stack on the 50000 task chain and ignores the alphabetical tie-break.
- Test to tighten: build four tasks in a loop with one task hanging off it, assert
  `has_cycle()` is True and that `execution_order()` raises.

---

Spoilers ahead: [`../../solutions/04_task_scheduler/ANSWER_KEY.md`](../../solutions/04_task_scheduler/ANSWER_KEY.md)
names both bugs, the whole optimization ladder and the expected values. Do not open it until
your timer is done.
