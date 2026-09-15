"""Generate the map files for the Route Planner problem.

Run from this directory: python gen_data.py
Only the small, medium and large maps are written; see src/map_data.py for the rest.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from map_data import grid  # noqa: E402


def write(name, stops, roads):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        for stop in stops:
            handle.write(f"stop {stop}\n")
        for a, b, minutes in roads:
            handle.write(f"road {a} {b} {minutes}\n")
    print(f"{name}: {len(stops)} stops, {len(roads)} roads, {os.path.getsize(path)} bytes")


def main():
    write("map_small.txt", *grid(4, 5, seed=21))
    write("map_medium.txt", *grid(30, 30, seed=22))
    write("map_large.txt", *grid(100, 100, seed=23))


if __name__ == "__main__":
    main()
