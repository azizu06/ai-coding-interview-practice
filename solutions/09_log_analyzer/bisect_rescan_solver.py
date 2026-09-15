"""Middle rung: sort the log once, then use bisect to find each window's slice
and rebuild the per endpoint groups from scratch for that slice.

Much better than scanning the whole log per window, but the work per window is
still proportional to how many requests the window holds. When the windows are
long and the step is short, the same request is regrouped and re-sorted in
hundreds of windows.
"""

import bisect

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
        result = []
        start = first
        while start <= last:
            low = bisect.bisect_left(times, start)
            high = bisect.bisect_left(times, start + width)
            groups = {}
            for index in range(low, high):
                _when, endpoint, latency = entries[index]
                bucket = groups.get(endpoint)
                if bucket is None:
                    bucket = groups[endpoint] = []
                bucket.append(latency)
            ranked = []
            for endpoint, values in groups.items():
                values.sort()
                ranked.append((-values[p95_index(len(values))], endpoint))
            ranked.sort()
            result.append([(endpoint, -score) for score, endpoint in ranked[:k]])
            start += step
        return result
