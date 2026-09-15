import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maze import Maze  # noqa: E402
from mazes import (  # noqa: E402
    get_example_maze,
    get_huge_maze,
    get_large_maze,
    get_medium_maze,
    get_small_maze,
)
from solver import Solver  # noqa: E402


def solve(text):
    return Solver(Maze.parse(text)).shortest_path()


class TestSolver(unittest.TestCase):
    def test_straight_corridor(self):
        self.assertEqual(solve("S..G"), 3)

    def test_start_next_to_exit(self):
        self.assertEqual(solve("SG"), 1)

    def test_walks_around_wall(self):
        text = """
        S#G
        ...
        """
        self.assertEqual(solve(text), 4)

    def test_no_route(self):
        text = """
        S#G
        .#.
        """
        self.assertEqual(solve(text), -1)

    def test_door_without_key_blocks(self):
        self.assertEqual(solve("SAG"), -1)

    # def test_key_on_the_way(self):
    #     expected = "????"
    #     self.assertEqual(solve("SaAG"), expected)

    # def test_must_detour_for_key(self):
    #     text = """
    #     S.AG
    #     .###
    #     a...
    #     """
    #     expected = "????"
    #     self.assertEqual(solve(text), expected)

    # def test_must_backtrack_through_visited_cells(self):
    #     # The key sits at a dead end behind the start. Cells near S are
    #     # walked twice: once to fetch the key, once on the way to the door.
    #     text = """
    #     a...S.AG
    #     """
    #     expected = "????"
    #     self.assertEqual(solve(text), expected)

    # def test_two_keys_chained(self):
    #     text = """
    #     S.A.B.G
    #     .#.#.#.
    #     a#b#...
    #     """
    #     expected = "????"
    #     self.assertEqual(solve(text), expected)

    # def test_example_maze(self):
    #     expected = "????"
    #     self.assertEqual(Solver(get_example_maze()).shortest_path(), expected)

    # # ---- timed tests: uncomment once the solver is correct ----------------

    # def test_small_maze_timed(self):
    #     maze = get_small_maze()
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     result = Solver(maze).shortest_path()
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(result, 32)
    #     self.assertLess(elapsed, expected_time, f"20x20 maze: {elapsed:.2f}s, need < {expected_time}s")

    # def test_medium_maze_timed(self):
    #     maze = get_medium_maze()
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     result = Solver(maze).shortest_path()
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(result, 126)
    #     self.assertLess(elapsed, expected_time, f"30x30 maze: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_maze_timed(self):
    #     maze = get_large_maze()
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     result = Solver(maze).shortest_path()
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(result, 388)
    #     self.assertLess(elapsed, expected_time, f"120x120 maze: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_maze_timed(self):
    #     maze = get_huge_maze()
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     result = Solver(maze).shortest_path()
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(result, 722)
    #     self.assertLess(elapsed, expected_time, f"300x300 maze, six keys: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
