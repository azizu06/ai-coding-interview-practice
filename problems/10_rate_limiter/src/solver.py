"""You'll implement this."""

from request_log import RequestLog


class Solver:
    def __init__(self, log: RequestLog):
        self.log = log

    def decide(self):
        """Decide every request in the log, in log order.

        Return a list of booleans, one per request, True when the request is
        allowed. A request is allowed only when it is within BOTH rules
        described at the top of `request_log.py`: the sliding window and the
        token bucket. Remember that every request counts toward its client's
        window whether or not it was allowed, and that only an allowed request
        spends tokens.

        Clients are independent of each other. An empty log gives an empty
        list.
        """
        pass
