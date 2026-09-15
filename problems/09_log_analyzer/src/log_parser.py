"""Read this first."""

import math

DAYS_BEFORE_MONTH = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
METHODS = ("GET", "POST", "PUT", "DELETE")


def p95_index(count):
    if count <= 0:
        raise ValueError("no values")
    return math.ceil(0.95 * count) - 1


class LogParser:
    def __init__(self):
        self._days_before_year = {}

    def is_leap_year(self, year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def days_before_year(self, year):
        cached = self._days_before_year.get(year)
        if cached is None:
            cached = 0
            for past in range(1970, year):
                cached += 366 if self.is_leap_year(past) else 365
            self._days_before_year[year] = cached
        return cached

    def to_epoch(self, stamp):
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
        parts = path.split("/")
        for i, part in enumerate(parts):
            if part.isdigit() and len(part) > 2:
                parts[i] = "{id}"
        return "/".join(parts)

    def parse_line(self, line):
        parts = line.split()
        if len(parts) != 5:
            return None
        stamp, method, path, status, latency = parts
        if method not in METHODS:
            return None
        if not status.isdigit() or not latency.isdigit():
            return None
        return (self.to_epoch(stamp), method, path, int(status), int(latency))
