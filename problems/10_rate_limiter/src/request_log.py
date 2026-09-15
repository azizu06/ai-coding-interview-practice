"""Read this first.

A request log for an API gateway. One request per line, three whitespace
separated fields:

    12.5 c0042 2

    when    seconds since the log started, written as whole seconds, a dot,
            and a decimal fraction of a second of one to three digits.
            `12.5` is 12500 ms, `12.05` is 12050 ms, `12.005` is 12005 ms.
    client  the client id
    weight  how much this request costs, a whole number of units

Every client has a limit, read from a second file with five fields:

    c0042 10000 60 20 8

    client           the client id, or `*` for the limit every other client gets
    window_ms        width of the sliding window, in milliseconds
    max_weight       total weight allowed inside the window
    capacity         size of the token bucket, in units
    refill_per_sec   units the bucket regains per second

Two rules run at once, and a request has to satisfy both to be allowed.

    sliding window  Every request inside the window counts against the limit,
                    allowed or not, because the window measures how hard the
                    client is knocking. A request of weight w arriving at time
                    t is within the rule when the weight of the requests in the
                    window that ends at t, this one included, is at most
                    `max_weight`.

    token bucket    The bucket starts full at `capacity` units and regains
                    `refill_per_sec` units per second, never going above
                    `capacity`. A request of weight w is within the rule when
                    the bucket holds at least w units at that moment. Only an
                    ALLOWED request spends its w units; a request turned away
                    by either rule spends nothing.

The window is half open. It ends at the arriving request and does not include
its own far edge, so a request exactly `window_ms` older than the arrival has
already left the window. `in_window` is the one place that decides this.

Tokens are counted in thousandths of a unit so that refilling stays exact
integer arithmetic. `refill` does that conversion.
"""

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
        """Milliseconds for a `seconds.fraction` timestamp."""
        whole, _, fraction = text.partition(".")
        return int(whole) * 1000 + int(fraction or "0")

    def parse(self, line):
        """Parse one request line.

        Return (millis, client, weight), or None when the line is blank or does
        not have the three expected fields.
        """
        parts = line.split()
        if len(parts) != 3:
            return None
        when, client, weight = parts
        if not weight.isdigit():
            return None
        return (self.to_millis(when), client, int(weight))

    def parse_limit(self, line):
        """Parse one limit line into (client, Limit), or None when malformed."""
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
        """The limit for `client`, or the default limit when it has none."""
        return self._limits.get(client, self._default)

    def clients(self):
        """Every client that sent a request, in ascending order."""
        return sorted(self._by_client)

    def requests(self):
        """Every request, in the order it appeared in the log."""
        return list(self._requests)

    def requests_for(self, client):
        """The requests sent by `client`, in log order."""
        return list(self._by_client.get(client, ()))

    def in_window(self, earlier, later, width_ms):
        """True when a request at `earlier` is still inside the window at `later`."""
        return later - earlier <= width_ms

    def refill(self, tokens_milli, elapsed_ms, limit):
        """Top up a bucket holding `tokens_milli` thousandths after `elapsed_ms`."""
        gained = elapsed_ms * limit.refill_per_sec
        ceiling = limit.capacity * 1000
        return min(ceiling, tokens_milli + gained)
