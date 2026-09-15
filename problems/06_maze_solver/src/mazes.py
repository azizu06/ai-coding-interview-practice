import os

from maze import Maze

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

EXAMPLE_TEXT = """
#########
#S..#..a#
#.#.#.#.#
#.#...#.#
#.#####.#
#...A..G#
#########
"""


def _load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as handle:
        return Maze.parse(handle.read())


def get_example_maze():
    return Maze.parse(EXAMPLE_TEXT)


def get_small_maze():
    return _load("maze_small.txt")


def get_medium_maze():
    return _load("maze_medium.txt")


def get_large_maze():
    return _load("maze_large.txt")


def get_huge_maze():
    return _load("maze_huge.txt")
