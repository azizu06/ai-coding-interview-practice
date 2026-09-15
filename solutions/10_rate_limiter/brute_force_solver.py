"""Naive solution: re-read the client's whole history for every request.

The window rule is answered by walking every request the client has ever sent
and keeping the ones still inside the window. That is correct and easy to read,
and it costs O(history) per request, so a busy client gets quadratically slower
as its history grows.
"""

from request_log import RequestLog


class Solver:
    def __init__(self, log: RequestLog):
        self.log = log

    def decide(self):
        log = self.log
        history = {}
        buckets = {}
        out = []
        for when, client, weight in log.requests():
            limit = log.limit_for(client)
            past = history.setdefault(client, [])
            past.append((when, weight))
            if client not in buckets:
                buckets[client] = [limit.capacity * 1000, when]

            total = 0
            for earlier, earlier_weight in past:
                if log.in_window(earlier, when, limit.window_ms):
                    total += earlier_weight

            bucket = buckets[client]
            tokens = log.refill(bucket[0], when - bucket[1], limit)
            allowed = total <= limit.max_weight and tokens >= weight * 1000
            if allowed:
                tokens -= weight * 1000
            bucket[0] = tokens
            bucket[1] = when
            out.append(allowed)
        return out
