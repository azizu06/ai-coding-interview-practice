"""Runnable demo. Try: python src/main.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maze import Maze  # noqa: E402
from mazes import get_example_maze  # noqa: E402
from solver import Solver  # noqa: E402


def main():
    print("=== BEGIN maze demo ===")
    maze = get_example_maze()
    print("Input maze:")
    print(maze)
    print()
    print(f"size: {maze.rows} rows x {maze.cols} cols")
    print(f"start: {maze.start}  exit: {maze.exit}")
    print(f"keys: {maze.keys}")
    print(f"doors: {maze.doors}")
    print()
    r, c = maze.start
    print(f"neighbors of start {maze.start} with no keys: {maze.neighbors(r, c)}")
    door = maze.doors["A"][0]
    print(f"door A at {door} open with no keys? {maze.is_open(*door)}")
    print(f"door A at {door} open with key a?  {maze.is_open(*door, keys=frozenset('a'))}")
    print()
    result = Solver(maze).shortest_path()
    print(f"Output: shortest path length = {result}")
    print("=== END maze demo ===")


if __name__ == "__main__":
    main()
