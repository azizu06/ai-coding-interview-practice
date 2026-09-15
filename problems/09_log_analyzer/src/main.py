"""Runnable demo. Try: python src/main.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_data import get_example_lines  # noqa: E402
from log_parser import LogParser, p95_index  # noqa: E402
from solver import Solver  # noqa: E402

SAMPLE_PATHS = [
    "/health",
    "/api/users/7",
    "/api/cart/42",
    "/api/orders/4812/items",
    "/static/app.js",
]


def main():
    print("=== BEGIN log analyzer demo ===")
    parser = LogParser()
    lines = get_example_lines()

    print("the example log:")
    for line in lines:
        print(f"    {line}")
    print()

    print("timestamps:")
    for stamp in ("2026-03-01T00:00:00Z", "2026-03-01T00:02:10Z", "2026-03-01T10:15:32Z"):
        print(f"    to_epoch({stamp}) = {parser.to_epoch(stamp)}")
    print()

    print("endpoints:")
    for path in SAMPLE_PATHS:
        print(f"    {path:24s} -> {parser.endpoint_of(path)}")
    print()

    print("p95 index by group size:")
    print(f"    {[(n, p95_index(n)) for n in (1, 2, 5, 10, 20, 21)]}")
    print()

    print("parsed rows:")
    for line in lines[:3]:
        print(f"    {parser.parse_line(line)}")
    print(f"    a junk line parses to {parser.parse_line('not a log line')}")
    print()

    solver = Solver(parser, lines)
    print(f"{len(solver.entries)} entries loaded")
    result = solver.scan_windows(60, 60, 3)
    if result is None:
        print("scan_windows is not implemented yet")
    else:
        for index, window in enumerate(result):
            print(f"    window {index}: {window}")
    print("=== END log analyzer demo ===")


if __name__ == "__main__":
    main()
