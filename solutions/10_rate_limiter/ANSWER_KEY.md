# 10 Rate Limiter: answer key

## The two bugs in `RequestLog`

1. `to_millis` adds the fraction without lining it up with the decimal point:

   ```python
   return int(whole) * 1000 + int(fraction or "0")
   ```

   A three digit fraction is right, which is why `12.005` and `12.500` both
   come out correct. Anything shorter is silently scaled down: `12.5` becomes
   12005 ms instead of 12500 ms. The generated logs write the shortest
   fraction that is exact, so most timestamps in them are one or two digits and
   the whole log collapses towards the start of each second. Fix: pad the
   fraction on the right before reading it,
   `int(((fraction or "0") + "000")[:3])`. Caught by
   `test_a_one_digit_fraction_is_tenths` and
   `test_a_two_digit_fraction_is_hundredths`.
2. `in_window` keeps a request that is exactly one window old:

   ```python
   return later - earlier <= width_ms
   ```

   The README says the window is half open, so a request exactly `window_ms`
   older than the arrival has already left. The bug only shows on
   an exact tie, which never happens in the hand written examples and happens
   constantly in the generated logs, where hundreds of pairs of requests land
   exactly one window apart. Fix: `<`. Caught by
   `test_a_request_exactly_one_window_old_has_left`,
   `test_the_far_edge_of_a_wider_window` and, through the solver,
   `test_the_far_edge_of_the_window`.

Filled-in `????` values live in `expected.json` in this folder.

The interacting rules are worth dwelling on. `test_the_two_rules_interact`
covers the case where the bucket has a token ready and the window refuses
anyway, and `test_a_denied_request_spends_nothing` covers the reverse: a
request the limiter turns away must not drain the bucket, or a client that is
being throttled can never recover.

## Brute force

`brute_force_solver.py` answers the window rule by walking the client's whole
history for every request and keeping the ones still inside the window. Correct,
and O(history) per request, so a client gets slower the longer it has been
sending.

It passes the 4000 and 40000 request tests (0.11 s on medium) and fails both
big ones: 2.1 s on the large log against a 1.0 s budget, and far past the
timeout on the hot log, where eight clients each build a history of 15000
requests.

## Optimization ladder

### Rung 1: re-read the client's whole history

The brute force above. Breaks on `test_large_300000_requests` and
`test_hot_eight_very_busy_clients`.

### Rung 2: evict with a deque, then add the window up

Keep a deque per client and pop from the front while the oldest request has
left the window. Nothing outside the window is ever touched again, which is
what the large log was waiting for: 2.1 s drops to 0.17 s.

The trap is that the window still has to be added up, and `sum(...)` over the
deque is O(window occupancy) per request. On the large log a window holds a
handful of requests, so nobody notices. On the hot log a window holds about
five hundred, and the same weights are added up again for every one of them.

Breaks on `test_hot_eight_very_busy_clients`: about 2.1 s against a 1.0 s
budget. See `window_resum_solver.py`.

### Rung 3: carry a running total, and refill lazily

Two changes make the cost per request constant:

* keep the total weight of the deque as a number, add the arriving weight to it
  and subtract each weight as it is popped, so the window is never re-read
* never tick the bucket forward. Store the tokens and the time of the client's
  previous request, and top the bucket up by the elapsed time only when that
  client is seen again

Every request is appended once and popped once across the whole run, however
many windows it belongs to, so the work no longer depends on how crowded a
window is. Tokens are kept in thousandths of a unit, which keeps the refill in
integers and out of floating point.

Cost: O(1) per request. About 0.08 s on the hot log. Reference: `solver.py`.

## Timed test summary (measured on this machine)

| test | requests | clients | budget | brute | rung 2 | reference |
| --- | --- | --- | --- | --- | --- | --- |
| small | 4000 | 300 | 1.0 s | 0.01 s | 0.00 s | 0.00 s |
| medium | 40000 | 800 | 1.0 s | 0.11 s | 0.02 s | 0.01 s |
| large | 300000 | 3000 | 1.0 s | 2.12 s | 0.17 s | 0.10 s |
| hot | 120000 | 8 | 1.0 s | over the timeout | 2.08 s | 0.08 s |

## Good AI prompts

1. "Here are the two rules from README.md. Restate them as a decision procedure
   for one request, being explicit about which requests count toward the window
   and which ones spend tokens."
2. "On the hot log each client's window holds around five hundred requests and
   I add them up on every request. Rewrite the window so each request is added
   to a total once and subtracted once."
3. "Replace my per millisecond bucket tick with a lazy refill computed from the
   gap since that client's previous request, in integer thousandths of a unit,
   and show me that the two agree on this log."

## Bad AI prompts

1. "Write a rate limiter." (You get one rule, usually a token bucket, and the
   window rule quietly disappears.)
2. "Only count allowed requests in the window." (A reasonable sounding guess,
   and the opposite of the rule the README states.)
3. "Fix the bugs in request_log.py." (Both bugs look deliberate: a timestamp
   parser that handles the format the examples use, and an inclusive window
   comparison that reads like a choice.)
