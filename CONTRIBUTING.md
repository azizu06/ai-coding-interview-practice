# Contributing

New problems are welcome. The only hard requirement is that `python tools/verify.py` passes
for whatever you add, because that script is what keeps every problem honest.

## The shape of a problem

A problem is two folders that share a slug of the form `NN_snake_case`:

```
problems/NN_slug/
  README.md            the problem, written to the same template as the others
  data/gen_data.py     the script that produced the committed data files
  data/*.txt           the committed fixtures
  src/main.py          a runnable demo that prints the domain class doing its job
  src/<domain>.py      the domain class, shipped with exactly two planted bugs
  src/<loaders>.py     loaders, plus in-memory builders for fixtures too big to commit
  src/solver.py        the stub a candidate completes
  src/test_<domain>.py unit tests for the domain class
  src/test_solver.py   correctness tests first, then timed tests

solutions/NN_slug/
  ANSWER_KEY.md            both bugs, the ladder with complexities, good and bad prompts
  expected.json            the value behind every ???? keyed by test method name
  solver.py                the reference solver
  brute_force_solver.py    the obvious solution that fails at least one timed test on time
  <domain>.py              a fixed copy of each domain file
  *_solver.py              optional middle rungs of the ladder
```

## Conventions the verifier depends on

`tools/verify.py` rewrites the source mechanically, so the files have to follow a few rules.
The full list lives in the module docstring at the top of that script. The ones people trip
over:

- A commented-out test starts with `    # def test_x(self):` and every following line of
  that test is `    # <code>` at the same indent. A blank line inside the block is a bare
  `    #`.
- An unknown expected value is its own assignment line, `expected = "????"`. The variable
  name has to contain `expected`. Its real value goes in `expected.json` under the test
  method name.
- A timed test contains `expected_time = <seconds>`. That number is the budget the verifier
  holds the reference solver and the brute force solver to.
- Heavy fixtures for timed tests belong in `setUpClass`, so the measured wall time reflects
  the solver rather than data loading.

`tools/run.py` leans on the same two conventions, because `run.py NN timed` reveals one
timed test at a time by uncommenting exactly one commented-out block. It finds the timed
tests by the `expected_time` assignment, and it expects them to sit in one commented block
at the bottom of `class TestSolverSpeed`, in ladder order, hardest last. Put them anywhere
else and `--list` will say so rather than guessing: problem 06 keeps its timed tests at the
bottom of `TestSolver` and gets that note today. New problems should use `TestSolverSpeed`.

## Writing the problem README

Copy the structure of an existing one, for example
[`problems/05_route_planner/README.md`](problems/05_route_planner/README.md). In order:
title, one-line pitch in italics, the key-value table, "The problem" with a worked example,
"The codebase" as a file table, "Your tasks" as six steps tagged by phase, "How to run",
"Hints for using your AI well", and the spoiler link to the answer key.

The three hints are the part worth spending time on. They should be specific to this
problem: what a good prompt looks like here, what an assistant reliably gets wrong here, and
which test is worth tightening. Write them after you have solved the problem with an agent,
not before.

House style: straight quotes, no em dashes or en dashes, no email addresses anywhere in the
repository.

## Before you open a pull request

```bash
python tools/verify.py
```

All four stages have to read `PASS` for every problem. If you only touched one problem, you
can name it while you iterate, then run the whole suite once at the end.

```bash
python tools/verify.py 05_route_planner
```

Also run the demo and the shipped tests by hand once, since the verifier works in a
temporary copy and will not catch a path that only breaks in place.

```bash
python problems/05_route_planner/src/main.py
python -m unittest discover -s problems/05_route_planner/src -v
```

Then check that the session tools see the new problem the way a candidate will. `start`
copies it into `workspace/`, which is git ignored, so this leaves `problems/` alone.

```bash
python tools/run.py 05 --list
python tools/session.py start 05 --minutes 1
python tools/run.py 05 timed
python tools/session.py reset 05
```

`--list` should name every timed test in ladder order under `TestSolverSpeed`, all hidden,
and `timed` should reveal the first one and nothing else.

Before the solver is implemented, `test_solver.py` failing is the correct shipped state. The
domain tests must pass.
