"""Runnable demo. Try: python src/main.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from request_log import RequestLog  # noqa: E402
from solver import Solver  # noqa: E402
from traffic_data import get_example_limits, get_example_requests  # noqa: E402


def main():
    print("=== BEGIN rate limiter demo ===")
    limits = get_example_limits()
    requests = get_example_requests()

    print("limits:")
    for line in limits:
        print(f"    {line}")
    print()
    print("requests:")
    for line in requests:
        print(f"    {line}")
    print()

    log = RequestLog(limits, requests)
    print("timestamps:")
    for text in ("0.0", "0.25", "12.5", "12.05", "12.005"):
        print(f"    to_millis({text}) = {log.to_millis(text)} ms")
    print()

    print("clients and their limits:")
    for client in log.clients():
        print(f"    {client:4s} {log.limit_for(client)}")
    print(f"    a client with no row of its own gets {log.limit_for('nobody')}")
    print()

    print("window edges, for a window 1000 ms wide:")
    for earlier in (0, 500, 999, 1000):
        print(f"    a request at {earlier:4d} ms, seen at 1000 ms: {log.in_window(earlier, 1000, 1000)}")
    print()

    decisions = Solver(log).decide()
    if decisions is None:
        print("decide is not implemented yet")
    else:
        print("decisions:")
        for (when, client, weight), allowed in zip(log.requests(), decisions):
            verdict = "allowed" if allowed else "denied"
            print(f"    {when:5d} ms  {client:4s} weight {weight}  {verdict}")
        print(f"{sum(decisions)} of {len(decisions)} requests allowed")
    print("=== END rate limiter demo ===")


if __name__ == "__main__":
    main()
