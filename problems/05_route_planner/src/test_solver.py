import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from map_data import (  # noqa: E402
    get_example_map,
    get_huge_map,
    get_huge_queries,
    get_huge_starts,
    get_large_map,
    get_large_queries,
    get_medium_map,
    get_medium_queries,
    get_small_map,
)
from road_map import RoadMap  # noqa: E402
from solver import Solver  # noqa: E402


def build_map(stops, roads):
    road_map = RoadMap()
    for stop in stops:
        road_map.add_stop(stop)
    for a, b, minutes in roads:
        road_map.add_road(a, b, minutes)
    return road_map


def example_solver():
    return Solver(build_map(*get_example_map()))


class TestShortestTime(unittest.TestCase):
    def test_a_stop_reaches_itself_in_no_time(self):
        self.assertEqual(example_solver().shortest_time("harbor", "harbor"), 0)

    def test_direct_road_is_the_whole_trip(self):
        self.assertEqual(example_solver().shortest_time("campus", "downtown"), 5)

    def test_isolated_stop_is_unreachable(self):
        solver = example_solver()
        self.assertIsNone(solver.shortest_time("island", "beach"))
        self.assertIsNone(solver.shortest_time("beach", "island"))

    def test_unknown_stop_is_unreachable(self):
        self.assertIsNone(example_solver().shortest_time("airport", "ghost"))

    # def test_two_hops_beat_one_slow_road(self):
    #     expected = "????"
    #     self.assertEqual(example_solver().shortest_time("airport", "downtown"), expected)

    # def test_longest_trip_in_town(self):
    #     expected = "????"
    #     self.assertEqual(example_solver().shortest_time("airport", "beach"), expected)

    # def test_route_around_the_bay(self):
    #     expected = "????"
    #     self.assertEqual(example_solver().shortest_time("airport", "harbor"), expected)

    # def test_small_grid_corner_to_corner(self):
    #     solver = Solver(build_map(*get_small_map()))
    #     expected = "????"
    #     self.assertEqual(solver.shortest_time("r0c0", "r3c4"), expected)


class TestNearestStops(unittest.TestCase):
    def test_zero_k_gives_nothing(self):
        self.assertEqual(example_solver().nearest_stops("downtown", 0), [])

    def test_results_are_ordered_by_minutes(self):
        found = example_solver().nearest_stops("campus", 4)
        self.assertEqual(found, sorted(found, key=lambda pair: (pair[1], pair[0])))

    def test_start_is_never_in_its_own_result(self):
        self.assertNotIn("campus", [stop for stop, _ in example_solver().nearest_stops("campus", 5)])

    # def test_three_nearest_to_downtown(self):
    #     expected = "????"
    #     self.assertEqual(example_solver().nearest_stops("downtown", 3), expected)

    # def test_isolated_stop_has_no_neighbours(self):
    #     expected = "????"
    #     self.assertEqual(example_solver().nearest_stops("island", 3), expected)

    # def test_asking_for_more_than_exists(self):
    #     expected = "????"
    #     self.assertEqual(example_solver().nearest_stops("airport", 10), expected)

    # def test_small_grid_nearest_three(self):
    #     solver = Solver(build_map(*get_small_map()))
    #     expected = "????"
    #     self.assertEqual(solver.nearest_stops("r0c0", 3), expected)


# Timed tests. Uncomment them for task 6.
#
# Every map is built once in setUpClass, so the clock only covers the queries themselves.
# Each test also checks the total of the answers, so a solver cannot win by being fast and
# wrong. The maps are grids: "r12c30" is row 12, column 30.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.medium = build_map(*get_medium_map())
        cls.large = build_map(*get_large_map())
        cls.huge = build_map(*get_huge_map())
        cls.medium_queries = get_medium_queries()
        cls.large_queries = get_large_queries()
        cls.huge_queries = get_huge_queries()
        cls.huge_starts = get_huge_starts()

    # def test_medium_900_stops(self):
    #     expected_time = 1.0
    #     expected = "????"
    #     solver = Solver(self.medium)
    #     start = time.perf_counter()
    #     total = sum(solver.shortest_time(a, b) for a, b in self.medium_queries)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected)
    #     self.assertLess(elapsed, expected_time, f"900 stops, 10 trips: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_10000_stops(self):
    #     expected_time = 1.0
    #     expected = "????"
    #     solver = Solver(self.large)
    #     start = time.perf_counter()
    #     total = sum(solver.shortest_time(a, b) for a, b in self.large_queries)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected)
    #     self.assertLess(elapsed, expected_time, f"10000 stops, 10 trips: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_90000_stops_short_trips(self):
    #     expected_time = 2.0
    #     expected = "????"
    #     solver = Solver(self.huge)
    #     start = time.perf_counter()
    #     total = sum(solver.shortest_time(a, b) for a, b in self.huge_queries)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected)
    #     self.assertLess(elapsed, expected_time, f"90000 stops, 100 short trips: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_90000_stops_nearest_five(self):
    #     expected_time = 1.0
    #     expected = "????"
    #     solver = Solver(self.huge)
    #     start = time.perf_counter()
    #     total = sum(minutes for stop in self.huge_starts for _, minutes in solver.nearest_stops(stop, 5))
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected)
    #     self.assertLess(elapsed, expected_time, f"90000 stops, 200 nearest-five queries: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
