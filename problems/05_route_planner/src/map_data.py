"""Loaders for the map files in ../data, plus generators for the huge grid and the queries.

Each map loader returns a pair `(stops, roads)`:
  * stops is a list of stop names
  * roads is a list of (a, b, minutes)

Maps are grids: stop "r3c7" is row 3, column 7, and roads join horizontal and vertical
neighbors with a random travel time from 1 to 9 minutes. The 300 by 300 grid would be a
4 MB file, so it is generated in memory from a fixed seed. Queries are generated the same
way. `grid` and `grid_queries` are also what data/gen_data.py uses.
"""

import os
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def stop_name(row, col):
    return f"r{row}c{col}"


def grid(rows, cols, seed):
    rng = random.Random(seed)
    stops = [stop_name(r, c) for r in range(rows) for c in range(cols)]
    roads = []
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                roads.append((stop_name(r, c), stop_name(r, c + 1), rng.randint(1, 9)))
            if r + 1 < rows:
                roads.append((stop_name(r, c), stop_name(r + 1, c), rng.randint(1, 9)))
    return stops, roads


def grid_queries(rows, cols, count, max_steps, seed):
    """(start, end) pairs. `max_steps` caps how far apart the two stops are on the grid."""
    rng = random.Random(seed)
    queries = []
    while len(queries) < count:
        r1, c1 = rng.randrange(rows), rng.randrange(cols)
        r2 = min(rows - 1, max(0, r1 + rng.randint(-max_steps, max_steps)))
        c2 = min(cols - 1, max(0, c1 + rng.randint(-max_steps, max_steps)))
        if (r1, c1) != (r2, c2):
            queries.append((stop_name(r1, c1), stop_name(r2, c2)))
    return queries


def grid_starts(rows, cols, count, seed):
    rng = random.Random(seed)
    return [stop_name(rng.randrange(rows), rng.randrange(cols)) for _ in range(count)]


def _read(name):
    stops = []
    roads = []
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as handle:
        for line in handle:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "stop":
                stops.append(parts[1])
            elif parts[0] == "road":
                roads.append((parts[1], parts[2], int(parts[3])))
    return stops, roads


def get_example_map():
    """The small town used in README.md and main.py."""
    stops = ["airport", "beach", "campus", "downtown", "harbor", "island"]
    roads = [
        ("airport", "downtown", 20),
        ("airport", "campus", 12),
        ("campus", "downtown", 5),
        ("downtown", "harbor", 8),
        ("campus", "beach", 15),
        ("harbor", "beach", 3),
    ]
    return stops, roads


def get_small_map():
    return _read("map_small.txt")


def get_medium_map():
    """30 by 30 grid, 900 stops."""
    return _read("map_medium.txt")


def get_large_map():
    """100 by 100 grid, 10000 stops."""
    return _read("map_large.txt")


def get_huge_map():
    """300 by 300 grid, 90000 stops, generated in memory."""
    return grid(300, 300, seed=20260907)


def get_medium_queries():
    return grid_queries(30, 30, 10, 30, seed=1)


def get_large_queries():
    return grid_queries(100, 100, 10, 100, seed=2)


def get_huge_queries():
    """100 trips on the huge grid, each between stops at most 15 rows and columns apart."""
    return grid_queries(300, 300, 100, 15, seed=3)


def get_huge_starts():
    """200 starting stops on the huge grid for nearest-stop queries."""
    return grid_starts(300, 300, 200, seed=4)
