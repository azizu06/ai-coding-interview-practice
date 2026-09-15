import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maze import Maze  # noqa: E402

TINY = """
S..
.#.
a.G
"""

WITH_DOOR = """
S.A.G
..#..
b.a..
"""


class TestMaze(unittest.TestCase):
    def test_parse_dimensions(self):
        maze = Maze.parse(TINY)
        self.assertEqual((maze.rows, maze.cols), (3, 3))

    def test_parse_finds_start_and_exit(self):
        maze = Maze.parse(TINY)
        self.assertEqual(maze.start, (0, 0))
        self.assertEqual(maze.exit, (2, 2))

    def test_parse_records_keys_and_doors(self):
        maze = Maze.parse(WITH_DOOR)
        self.assertEqual(maze.keys, {"a": (2, 2), "b": (2, 0)})
        self.assertEqual(maze.doors, {"A": [(0, 2)]})
        self.assertEqual(maze.all_keys(), ["a", "b"])

    def test_wall_is_not_open(self):
        maze = Maze.parse(TINY)
        self.assertFalse(maze.is_open(1, 1))

    def test_floor_and_start_are_open(self):
        maze = Maze.parse(TINY)
        self.assertTrue(maze.is_open(0, 1))
        self.assertTrue(maze.is_open(0, 0))

    def test_out_of_bounds_is_not_open(self):
        maze = Maze.parse(TINY)
        self.assertFalse(maze.is_open(-1, 0))
        self.assertFalse(maze.is_open(0, 3))

    def test_key_at(self):
        maze = Maze.parse(TINY)
        self.assertEqual(maze.key_at(2, 0), "a")
        self.assertIsNone(maze.key_at(0, 0))

    def test_neighbors_of_interior_cell(self):
        maze = Maze.parse(TINY)
        self.assertEqual(maze.neighbors(1, 0), [(0, 0), (2, 0)])

    def test_door_is_closed_without_key(self):
        maze = Maze.parse(WITH_DOOR)
        self.assertFalse(maze.is_open(0, 2))

    # def test_door_is_open_with_key(self):
    #     maze = Maze.parse(WITH_DOOR)
    #     expected = "????"
    #     self.assertEqual(maze.is_open(0, 2, keys=frozenset("a")), expected)

    # def test_door_stays_closed_with_wrong_key(self):
    #     maze = Maze.parse(WITH_DOOR)
    #     expected = "????"
    #     self.assertEqual(maze.is_open(0, 2, keys=frozenset("b")), expected)

    # def test_neighbors_in_last_column(self):
    #     maze = Maze.parse(TINY)
    #     expected = "????"
    #     self.assertEqual(maze.neighbors(0, 2), expected)

    # def test_neighbors_through_door_with_key(self):
    #     maze = Maze.parse(WITH_DOOR)
    #     expected = "????"
    #     self.assertEqual(maze.neighbors(0, 1, keys=frozenset("a")), expected)


if __name__ == "__main__":
    unittest.main()
