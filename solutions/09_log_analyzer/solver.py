"""Reference solution: slide the window instead of rebuilding it.

Sort the log once by time. Keep the requests currently inside the window in a
per endpoint list that is held sorted with bisect.insort. Moving the window
forward adds the requests that just came into range and removes the ones that
just left, so every request is inserted once and removed once no matter how
many windows overlap it.

With the latencies already sorted, the p95 of an endpoint is one index lookup.
"""

import bisect
import heapq

from log_parser import LogParser, p95_index


class Solver:
    def __init__(self, parser: LogParser, lines):
        self.parser = parser
        self.entries = []
        for line in lines:
            row = parser.parse_line(line)
            if row is None:
                continue
            epoch, _method, path, _status, latency = row
            self.entries.append((epoch, parser.endpoint_of(path), latency))

    def scan_windows(self, width, step, k):
        entries = sorted(self.entries)
        if not entries:
            return []
        times = [entry[0] for entry in entries]
        first = times[0]
        last = times[-1]
        count = len(entries)

        live = {}
        low = 0
        high = 0
        result = []
        start = first
        insort = bisect.insort
        bisect_left = bisect.bisect_left
        while start <= last:
            end = start + width
            while high < count and times[high] < end:
                _when, endpoint, latency = entries[high]
                values = live.get(endpoint)
                if values is None:
                    values = live[endpoint] = []
                insort(values, latency)
                high += 1
            while low < high and times[low] < start:
                _when, endpoint, latency = entries[low]
                values = live[endpoint]
                del values[bisect_left(values, latency)]
                if not values:
                    del live[endpoint]
                low += 1
            ranked = heapq.nsmallest(
                k,
                (
                    (-values[p95_index(len(values))], endpoint)
                    for endpoint, values in live.items()
                ),
            )
            result.append([(endpoint, -score) for score, endpoint in ranked])
            start += step
        return result
