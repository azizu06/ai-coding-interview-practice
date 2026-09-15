"""Rung 2: a real sliding window, but the window is re-read every request.

Old requests are evicted with a deque, so nothing outside the window is ever
looked at, which is already a large win over rescanning the client's whole
history. What it still does is add up the weights in the window from scratch
on every request, so the cost per request is the number of requests currently
in that client's window rather than a constant.
"""

from collections import deque

from request_log import RequestLog


class Solver:
    def __init__(self, log: RequestLog):
        self.log = log

    def decide(self):
        log = self.log
        windows = {}
        buckets = {}
        out = []
        for when, client, weight in log.requests():
            limit = log.limit_for(client)
            window = windows.get(client)
            if window is None:
                window = deque()
                windows[client] = window
                buckets[client] = [limit.capacity * 1000, when]

            while window and not log.in_window(window[0][0], when, limit.window_ms):
                window.popleft()
            window.append((when, weight))
            total = sum(item[1] for item in window)

            bucket = buckets[client]
            tokens = log.refill(bucket[0], when - bucket[1], limit)
            allowed = total <= limit.max_weight and tokens >= weight * 1000
            if allowed:
                tokens -= weight * 1000
            bucket[0] = tokens
            bucket[1] = when
            out.append(allowed)
        return out
