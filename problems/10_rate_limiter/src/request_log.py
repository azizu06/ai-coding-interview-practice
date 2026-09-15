"""Read this first."""

from collections import namedtuple

Limit = namedtuple("Limit", "window_ms max_weight capacity refill_per_sec")

DEFAULT_KEY = "*"
FALLBACK = Limit(window_ms=10000, max_weight=8, capacity=3, refill_per_sec=1)


class RequestLog:
    def __init__(self, limit_lines, request_lines):
        self._limits = {}
        self._default = FALLBACK
        for line in limit_lines:
            row = self.parse_limit(line)
            if row is None:
                continue
            client, limit = row
            if client == DEFAULT_KEY:
                self._default = limit
            else:
                self._limits[client] = limit

        self._requests = []
        self._by_client = {}
        for line in request_lines:
            row = self.parse(line)
            if row is None:
                continue
            self._requests.append(row)
            self._by_client.setdefault(row[1], []).append(row)

    def to_millis(self, text):
        whole, _, fraction = text.partition(".")
        return int(whole) * 1000 + int(fraction or "0")

    def parse(self, line):
        parts = line.split()
        if len(parts) != 3:
            return None
        when, client, weight = parts
        if not weight.isdigit():
            return None
        return (self.to_millis(when), client, int(weight))

    def parse_limit(self, line):
        parts = line.split()
        if len(parts) != 5:
            return None
        client = parts[0]
        numbers = parts[1:]
        if not all(value.isdigit() for value in numbers):
            return None
        window_ms, max_weight, capacity, refill = (int(value) for value in numbers)
        return (client, Limit(window_ms, max_weight, capacity, refill))

    def limit_for(self, client):
        return self._limits.get(client, self._default)

    def clients(self):
        return sorted(self._by_client)

    def requests(self):
        return list(self._requests)

    def requests_for(self, client):
        return list(self._by_client.get(client, ()))

    def in_window(self, earlier, later, width_ms):
        return later - earlier <= width_ms

    def refill(self, tokens_milli, elapsed_ms, limit):
        gained = elapsed_ms * limit.refill_per_sec
        ceiling = limit.capacity * 1000
        return min(ceiling, tokens_milli + gained)
