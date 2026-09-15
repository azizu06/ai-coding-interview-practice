# 09 Log Analyzer: answer key

## The two bugs in `LogParser`

1. `to_epoch` multiplies the hour by 360 instead of 3600:

   ```python
   return days * 86400 + hour * 360 + minute * 60 + second
   ```

   Every stamp in the first hour of a day is correct, which is why the shipped
   tests and the example log say nothing about it. Anything later in the day is
   shifted backwards, and since the generated logs run over four hours, the
   window boundaries land in the wrong places and the p95 checksums are wrong.
   Fix: `hour * 3600`. Caught by
   `test_an_hour_is_thirty_six_hundred_seconds` and
   `test_a_stamp_late_in_the_day`.
2. `endpoint_of` only collapses numeric segments of three digits or more:

   ```python
   if part.isdigit() and len(part) > 2:
   ```

   The docstring says every numeric segment. With the bug, `/api/users/7` and
   `/api/users/812` are counted as different endpoints, so the small id traffic
   the generator deliberately mixes in is scattered across hundreds of one-off
   groups, each with a p95 of its own single request. Fix: drop the length
   check and test `part.isdigit()` alone. Caught by
   `test_a_one_digit_id_is_still_an_id` and
   `test_a_two_digit_id_is_still_an_id`.

Filled-in `????` values live in `expected.json` in this folder.

Worth noting: the p95 here is nearest rank, `ceil(0.95 * n) - 1`. An assistant
asked for "p95 latency" will usually produce a linear interpolation instead, and
every checksum in the timed tests will then be off.

## Brute force

`brute_force_solver.py` walks the whole entry list once per window and keeps the
ones inside `[start, start + width)`. Cost is `O(windows * requests)`, and the
sorting per endpoint group is redone from nothing every window.

It passes the 2000 and 15000 request tests and fails the two 200000 request
tests: 3.2 s on the large log against a 1.0 s budget, and 6.7 s on the wide log.

## Optimization ladder

### Rung 1: re-scan every entry per window

The brute force above. Breaks on `test_large_200000_requests`, and breaks worse
on `test_wide_1440_overlapping_windows`.

### Rung 2: sort once, then binary search the window

Sort the entries by time once in the constructor, then per window use
`bisect_left` to find the slice `[start, start + width)` and only touch those
rows. That removes the scan over the whole log, so the large log drops from
3.2 s to 0.31 s and passes.

It still rebuilds the per endpoint lists and sorts each one from scratch for
every window. When windows overlap heavily that work is almost entirely
repeated: on the wide log each request sits in 180 windows, so the same
latencies are sorted 180 times.

Breaks on `test_wide_1440_overlapping_windows`: about 2.5 s against a 1.0 s
budget. See `bisect_rescan_solver.py`.

### Rung 3: carry the window along

A sliding window does not need to be rebuilt, only edited. Keep a `live` mapping
of endpoint to a sorted list of the latencies currently inside the window, plus
two pointers into the sorted entries:

* advance the high pointer and `bisect.insort` each entry that just entered
* advance the low pointer and delete each entry that just left, finding it with
  `bisect_left` on its own endpoint list
* drop an endpoint from `live` when its list empties

Each entry is inserted once and removed once over the whole scan, no matter how
many windows it belongs to, so the cost stops depending on the overlap. Ranking
a window is then `heapq.nsmallest(k, ...)` over the endpoints that are actually
live, reading each p95 straight out of its already sorted list by index.

Cost: `O(n log n + windows * live_endpoints)`. About 0.17 s on the wide log.
Reference: `solver.py`.

## Timed test summary (measured on this machine)

| test | requests | width / step | windows | budget | brute | rung 2 | reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| small | 2000 | 120 / 30 | 20 | 1.0 s | 0.00 s | 0.00 s | 0.00 s |
| medium | 15000 | 300 / 60 | 60 | 1.0 s | 0.02 s | 0.01 s | 0.01 s |
| large | 200000 | 300 / 15 | 960 | 1.0 s | 3.22 s | 0.31 s | 0.09 s |
| wide | 200000 | 900 / 5 | 1440 | 1.0 s | 6.68 s | 2.45 s | 0.17 s |

## Good AI prompts

1. "Read log_parser.py and state the exact definition of p95 used here, then
   write a one line function for it. Do not use numpy or a percentile formula
   from memory."
2. "On the wide log each request belongs to about 180 windows. Rewrite the scan
   so a request is added to the window state once and removed once, rather than
   being re-read for every window it touches."
3. "Here is my `live` dict of endpoint to sorted latency list. Give me the
   removal path: I know the endpoint and the latency, and there may be
   duplicates."

## Bad AI prompts

1. "Compute the p95 latency per endpoint." (You get an interpolated percentile,
   which disagrees with `p95_index` on almost every group size.)
2. "Make the sliding window faster." (Without naming the overlap, the usual
   answer is a faster inner sort, which is rung 2 again.)
3. "Fix the bugs in log_parser.py." (Both bugs look deliberate: an hour factor
   that is merely wrong, and a length check that reads like a guard against
   collapsing version numbers.)
