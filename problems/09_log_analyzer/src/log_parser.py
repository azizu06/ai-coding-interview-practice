"""Read this first.

A web server log. One request per line, five whitespace separated fields:

    2026-03-01T10:15:32Z GET /api/orders/4812/items 200 137

    timestamp   ISO 8601, always UTC, always whole seconds, always 20 chars
    method      GET, POST, PUT, DELETE
    path        the requested path
    status      the HTTP status code
    latency_ms  how long the request took, in whole milliseconds

Two paths that differ only in an id are the same endpoint, so `endpoint_of`
collapses every numeric path segment to the literal `{id}`:

    /api/orders/4812/items  ->  /api/orders/{id}/items
    /api/users/7            ->  /api/users/{id}

The p95 of a group of latencies is defined here by nearest rank: sort them
ascending and take the value at index `p95_index(len(values))`. That index is
`ceil(0.95 * n) - 1`, so a single request is its own p95 and a group of twenty
takes the value at index 18, the second largest of the twenty.
"""

import math

DAYS_BEFORE_MONTH = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
METHODS = ("GET", "POST", "PUT", "DELETE")


def p95_index(count):
    """Index of the p95 value in a list of `count` values sorted ascending."""
    if count <= 0:
        raise ValueError("no values")
    return math.ceil(0.95 * count) - 1


class LogParser:
    def __init__(self):
        self._days_before_year = {}

    def is_leap_year(self, year):
        """True for a leap year on the Gregorian calendar."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def days_before_year(self, year):
        """Whole days from 1970-01-01 to the first of January of `year`."""
        cached = self._days_before_year.get(year)
        if cached is None:
            cached = 0
            for past in range(1970, year):
                cached += 366 if self.is_leap_year(past) else 365
            self._days_before_year[year] = cached
        return cached

    def to_epoch(self, stamp):
        """Seconds from 1970-01-01T00:00:00Z to `stamp`."""
        year = int(stamp[0:4])
        month = int(stamp[5:7])
        day = int(stamp[8:10])
        hour = int(stamp[11:13])
        minute = int(stamp[14:16])
        second = int(stamp[17:19])
        days = self.days_before_year(year) + DAYS_BEFORE_MONTH[month - 1] + day - 1
        if month > 2 and self.is_leap_year(year):
            days += 1
        return days * 86400 + hour * 360 + minute * 60 + second

    def endpoint_of(self, path):
        """Collapse every numeric segment of `path` to `{id}`."""
        parts = path.split("/")
        for i, part in enumerate(parts):
            if part.isdigit() and len(part) > 2:
                parts[i] = "{id}"
        return "/".join(parts)

    def parse_line(self, line):
        """Parse one log line.

        Return (epoch, method, path, status, latency_ms), or None when the line
        is blank or does not have the five expected fields.
        """
        parts = line.split()
        if len(parts) != 5:
            return None
        stamp, method, path, status, latency = parts
        if method not in METHODS:
            return None
        if not status.isdigit() or not latency.isdigit():
            return None
        return (self.to_epoch(stamp), method, path, int(status), int(latency))
