"""Reference solution.

One pass over the log. Each client carries a deque of the requests inside its
window together with a running total of their weight, so a request costs one
append, one subtraction per departure, and nothing else. Every request enters
the deque once and leaves it once over the whole run, no matter how many
windows it sits in.

The bucket is lazy: instead of ticking it forward, each request tops it up for
the time since that client's previous request. Tokens are thousandths of a
unit, so the arithmetic stays exact.
"""

from collections import deque

from request_log import RequestLog


class Solver:
    def __init__(self, log: RequestLog):
        self.log = log

    def decide(self):
        log = self.log
        in_window = log.in_window
        refill = log.refill
        state = {}
        out = []
        for when, client, weight in log.requests():
            entry = state.get(client)
            if entry is None:
                limit = log.limit_for(client)
                entry = [deque(), 0, limit.capacity * 1000, when, limit]
                state[client] = entry
            window, total, tokens, last, limit = entry

            width = limit.window_ms
            while window and not in_window(window[0][0], when, width):
                total -= window.popleft()[1]
            window.append((when, weight))
            total += weight

            tokens = refill(tokens, when - last, limit)
            allowed = total <= limit.max_weight and tokens >= weight * 1000
            if allowed:
                tokens -= weight * 1000

            entry[1] = total
            entry[2] = tokens
            entry[3] = when
            out.append(allowed)
        return out
