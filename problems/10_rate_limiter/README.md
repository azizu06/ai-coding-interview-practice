# 10 Rate Limiter

*Replay a gateway log and decide, request by request, what should have been let through.*

|  |  |
| --- | --- |
| **Difficulty** | Hard |
| **Files you edit** | `src/request_log.py`, `src/solver.py` |
| **Suggested time** | 50 min |

## The problem

An API gateway writes down every request it receives. Each client has a limit. Your job is
to replay the log and say, for every request, whether the gateway should have let it through.

The log holds one request per line, three whitespace separated fields.

```
12.5 c0042 2
```

The first field is when the request arrived, given as seconds since the log started and
written as whole seconds, a dot, and one to three decimal digits. `12.5` is 12500 ms,
`12.05` is 12050 ms, and `12.005` is 12005 ms. The second field is the client id. The third
is the weight, how much the request costs, as a whole number of units.

A second file holds the limits, one client per line, five fields.

```
c0042 10000 60 20 8
```

Those five are the client id, the width of the sliding window in milliseconds, the total
weight allowed inside that window, the size of the token bucket in units, and the units the
bucket regains per second. A client id of `*` stands for the limit every other client gets.

Two rules run at once and a request has to satisfy both.

The sliding window counts every request inside the window against the limit, allowed or not,
because the window measures how hard the client is knocking. A request of weight w arriving
at time t is within the rule when the weight of the requests in the window ending at t, this
one included, is at most `max_weight`. The window is half open. It ends at the arriving
request and does not include its own far edge, so a request exactly `window_ms` older than
the arrival has already left the window.

The token bucket starts full at `capacity` and regains `refill_per_sec` units per second,
never going above `capacity`. A request of weight w is within the rule when the bucket holds
at least w units at that moment. Only an allowed request spends its w units, and a request
turned away by either rule spends nothing.

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

ada spends her three tokens on her first three requests and only earns one back per second,
so the requests at 0.3 and 0.4 have nothing to pay with. By 1.0 she has earned a whole token
again, but by then five of her requests sit inside the one second window, which is a weight
of 5 against a limit of 4, so the window turns it away instead. cy has no limit row of her
own, so she gets the default bucket of 2 units and cannot afford a weight 3 request.

## The codebase

| File | What it holds |
| --- | --- |
| `data/requests_small.txt` | 4000 requests from 300 clients over 60 seconds |
| `data/limits_small.txt` | the limit for each of those clients |
| `data/gen_data.py` | the script that produced the files above |
| `src/main.py` | runnable demo |
| `src/request_log.py` | the `RequestLog` class, which parses the log and the limits |
| `src/traffic_data.py` | loaders, and the builders for the three big logs |
| `src/solver.py` | the Solver stub you complete |
| `src/test_request_log.py` | unit tests for RequestLog |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

The three bigger logs are not committed, since as text they would be many megabytes.
`src/traffic_data.py` rebuilds them from fixed seeds: 40000 requests from 800 clients,
300000 requests from 3000 clients, and 120000 requests from eight clients.

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `RequestLog` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `decide()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/10_rate_limiter/src/main.py
python -m unittest discover -s problems/10_rate_limiter/src -v
```

From inside `problems/10_rate_limiter/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_request_log -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

---

Spoilers ahead: [`../../solutions/10_rate_limiter/ANSWER_KEY.md`](../../solutions/10_rate_limiter/ANSWER_KEY.md).
Do not open it until your timer is done.
