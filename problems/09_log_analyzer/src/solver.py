"""You'll implement this."""

from log_parser import LogParser


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
        """Walk a sliding window over the log and rank endpoints by p95 latency.

        The first window starts at the earliest timestamp in the log. Each one
        after it starts `step` seconds later, and the last window is the one
        whose start is still at or before the latest timestamp. A window covers
        `[start, start + width)`, so its end is not included.

        For every window, look at the requests inside it, group them by
        endpoint, and work out each endpoint's p95 latency using
        `log_parser.p95_index`. Keep the `k` endpoints with the highest p95,
        highest first, breaking ties by endpoint name in alphabetical order.

        Return one list of (endpoint, p95) pairs per window, in window order.
        A window with no requests contributes an empty list.
        An empty log gives an empty result.
        """
        pass
