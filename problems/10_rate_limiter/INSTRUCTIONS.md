# 10 Rate Limiter

Difficulty: Hard

## Problem

An API gateway writes down every request it receives. Each client has a limit.
Your job is to replay the log and say, for every request, whether the gateway
should have let it through.

Two rules run at once and a request has to satisfy both: a sliding window over
the client's recent traffic, and a token bucket that refills over time. Both
rules, the log format and the limit format are written out at the top of
`src/request_log.py`. Read them first. Two details there are easy to assume
your way past: the window counts every request, allowed or not, while only an
allowed request spends tokens.

## Example

```
limits (client, window_ms, max_weight, capacity, refill_per_sec):
  *    1000 4 2 2
  ada  1000 4 3 1
  bob  2000 3 2 4

requests:
  0.0   ada 1   allowed
  0.1   ada 1   allowed
  0.2   ada 1   allowed
  0.25  bob 1   allowed
  0.3   ada 1   denied
  0.4   ada 1   denied
  0.75  bob 2   allowed
  1.0   ada 1   denied
  1.2   bob 1   denied
  1.5   cy  3   denied
```

ada spends her three tokens on her first three requests and only earns one back
per second, so the requests at 0.3 and 0.4 have nothing to pay with. By 1.0 she
has earned a whole token again, but by then five of her requests sit inside the
one second window, which is a weight of 5 against a limit of 4, so the window
turns it away instead. cy has no limit row of her own, so she gets the default
bucket of 2 units and cannot afford a weight 3 request.

## Files

```
data/requests_small.txt   4000 requests from 300 clients over 60 seconds
data/limits_small.txt     the limit for each of those clients
data/gen_data.py          the script that produced the files above
src/request_log.py        the log format, the limits and the two rules (read this first)
src/traffic_data.py       loaders, and the builders for the three big logs
src/main.py               runnable demo
src/solver.py             the Solver stub you complete
src/test_request_log.py   unit tests for RequestLog
src/test_solver.py        unit tests for Solver, correctness first, then timed
```

The three bigger logs are not committed, since as text they would be many
megabytes. `src/traffic_data.py` rebuilds them from fixed seeds: 40000 requests
from 800 clients, 300000 requests from 3000 clients, and 120000 requests from
only eight clients. That last one is the smaller of the two big logs, but with
eight clients sharing it every client's window is crowded.

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `RequestLog` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `decide()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as
you would in the real interview. Start a 50 minute timer.
