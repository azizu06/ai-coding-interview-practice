# 09 Log Analyzer

Difficulty: Medium-Hard

## Problem

You have a web server log and a question about it: over a sliding window, which
endpoints are the slowest? Your job is to answer that question for every window
in the log.

The log format, the rule for turning a path into an endpoint, and the exact
definition of p95 all live in `src/log_parser.py`. Read them first. The p95 here
is nearest rank, not an interpolated percentile, so do not let an assistant swap
in the formula it remembers from somewhere else.

`scan_windows(width, step, k)` walks a window of `width` seconds across the log,
moving it forward `step` seconds at a time, and reports the `k` slowest
endpoints in each window. The docstring on the stub pins down where the first
window starts, where the last one ends, and what happens to an empty window.

## Example

```
log:
  2026-03-01T00:00:00Z GET  /api/users/7       200  40
  2026-03-01T00:00:10Z GET  /api/users/812     200  60
  2026-03-01T00:00:20Z GET  /api/search        200  900
  2026-03-01T00:00:30Z POST /api/orders/55     201  120
  2026-03-01T00:00:45Z GET  /health            200  2
  2026-03-01T00:01:05Z GET  /api/search        200  100
  2026-03-01T00:01:20Z GET  /api/users/9       200  55
  2026-03-01T00:01:40Z POST /api/orders/9001   201  400
  2026-03-01T00:01:55Z GET  /health            200  3
  2026-03-01T00:02:10Z GET  /api/search        500  1500

scan_windows(60, 60, 3):
  [('/api/search', 900), ('/api/orders/{id}', 120), ('/api/users/{id}', 60)]
  [('/api/orders/{id}', 400), ('/api/search', 100), ('/api/users/{id}', 55)]
  [('/api/search', 1500)]
```

`/api/users/7` and `/api/users/812` are the same endpoint, so the first window
sees two requests for `/api/users/{id}` at 40 ms and 60 ms. Two values put the
p95 at index 1, which is 60.

## Files

```
data/log_small.txt      2000 requests over 10 minutes
data/gen_data.py        the script that produced the file above
src/log_parser.py       the log format, endpoints and p95 (read this first)
src/log_data.py         loaders, and the builders for the three big logs
src/main.py             runnable demo
src/solver.py           the Solver stub you complete
src/test_log_parser.py  unit tests for LogParser
src/test_solver.py      unit tests for Solver, correctness first, then timed
```

The three bigger logs are not committed, since as text they would be tens of
megabytes. `src/log_data.py` rebuilds them from fixed seeds: 15000 requests over
an hour, 200000 requests over four hours, and 200000 requests over two hours.
The last one is no bigger than the one before it, but the timed test that uses
it asks for fifteen minute windows five seconds apart, so every request lands in
a great many windows at once.

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `LogParser` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `scan_windows()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as
you would in the real interview. Start a 50 minute timer.
