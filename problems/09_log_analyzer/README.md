# 09 Log Analyzer

*Slide a window across a server log and report the slowest endpoints in each one.*

|  |  |
| --- | --- |
| **Difficulty** | Medium-Hard |
| **Files you edit** | `src/log_parser.py`, `src/solver.py` |
| **Suggested time** | 50 min |

## The problem

You have a web server log and a question about it: over a sliding window, which endpoints
are the slowest? Your job is to answer that question for every window in the log.

The log holds one request per line, five whitespace separated fields.

```
2026-03-01T10:15:32Z GET /api/orders/4812/items 200 137

timestamp   ISO 8601, always UTC, always whole seconds, always 20 chars
method      GET, POST, PUT, DELETE
path        the requested path
status      the HTTP status code
latency_ms  how long the request took, in whole milliseconds
```

Two paths that differ only in an id are the same endpoint, so every numeric path segment
collapses to the literal `{id}`. That makes `/api/orders/4812/items` into
`/api/orders/{id}/items`, and `/api/users/7` into `/api/users/{id}`.

The p95 of a group of latencies is nearest rank, not an interpolated percentile. Sort the
latencies ascending and take the value at index `ceil(0.95 * n) - 1`, so a single request is
its own p95 and a group of twenty takes the value at index 18, the second largest of the
twenty.

`scan_windows(width, step, k)` walks a window of `width` seconds across the log, moving it
forward `step` seconds at a time, and reports the `k` slowest endpoints in each window. The
docstring on the stub pins down where the first window starts, where the last one ends, and
what happens to an empty window.

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

`/api/users/7` and `/api/users/812` are the same endpoint, so the first window sees two
requests for `/api/users/{id}` at 40 ms and 60 ms. Two values put the p95 at index 1, which
is 60.

## The codebase

| File | What it holds |
| --- | --- |
| `data/log_small.txt` | 2000 requests over 10 minutes |
| `data/gen_data.py` | the script that produced the file above |
| `src/main.py` | runnable demo |
| `src/log_parser.py` | `LogParser` and the p95 index helper |
| `src/log_data.py` | loaders, and the builders for the three big logs |
| `src/solver.py` | the Solver stub you complete |
| `src/test_log_parser.py` | unit tests for LogParser |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

The three bigger logs are not committed, since as text they would be tens of megabytes.
`src/log_data.py` rebuilds them from fixed seeds: 15000 requests over an hour, 200000
requests over four hours, and 200000 requests over two hours.

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `LogParser` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `scan_windows()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

From the repository root:

```bash
python problems/09_log_analyzer/src/main.py
python -m unittest discover -s problems/09_log_analyzer/src -v
```

From inside `problems/09_log_analyzer/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_log_parser -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

---

Spoilers ahead: [`../../solutions/09_log_analyzer/ANSWER_KEY.md`](../../solutions/09_log_analyzer/ANSWER_KEY.md).
Do not open it until your timer is done.
