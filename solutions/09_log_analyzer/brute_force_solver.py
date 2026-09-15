"""Brute force: for every window, walk the whole log and keep the requests
whose timestamp falls inside it.

Cost is O(windows * requests) before any sorting. Simple and obviously correct,
and it stops being usable as soon as the log grows past a few tens of thousands
of lines.
"""

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
        if not self.entries:
            return []
        first = min(entry[0] for entry in self.entries)
        last = max(entry[0] for entry in self.entries)
        result = []
        start = first
        while start <= last:
            end = start + width
            groups = {}
            for when, endpoint, latency in self.entries:
                if start <= when < end:
                    groups.setdefault(endpoint, []).append(latency)
            ranked = []
            for endpoint, values in groups.items():
                values.sort()
                ranked.append((-values[p95_index(len(values))], endpoint))
            ranked.sort()
            result.append([(endpoint, -score) for score, endpoint in ranked[:k]])
            start += step
        return result
