import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from map_data import get_example_map  # noqa: E402
from road_map import RoadMap  # noqa: E402


def example():
    """The six stop town from INSTRUCTIONS.md. `island` has no roads at all."""
    stops, roads = get_example_map()
    road_map = RoadMap()
    for stop in stops:
        road_map.add_stop(stop)
    for a, b, minutes in roads:
        road_map.add_road(a, b, minutes)
    return road_map


class TestAddStop(unittest.TestCase):
    def test_new_map_is_empty(self):
        road_map = RoadMap()
        self.assertEqual(len(road_map), 0)
        self.assertEqual(road_map.stops(), [])

    def test_add_stop_twice_is_harmless(self):
        road_map = RoadMap()
        road_map.add_stop("depot")
        road_map.add_stop("depot")
        self.assertEqual(len(road_map), 1)
        self.assertIn("depot", road_map)
        self.assertNotIn("ghost", road_map)

    def test_stops_are_sorted(self):
        road_map = example()
        self.assertEqual(road_map.stops(),
                         ["airport", "beach", "campus", "downtown", "harbor", "island"])


class TestAddRoad(unittest.TestCase):
    def test_unknown_stop_is_rejected(self):
        road_map = example()
        with self.assertRaises(KeyError):
            road_map.add_road("airport", "ghost", 5)
        with self.assertRaises(KeyError):
            road_map.add_road("ghost", "airport", 5)

    def test_self_road_is_rejected(self):
        road_map = example()
        with self.assertRaises(ValueError):
            road_map.add_road("airport", "airport", 5)

    def test_bad_minutes_is_rejected(self):
        road_map = example()
        with self.assertRaises(ValueError):
            road_map.add_road("airport", "beach", 0)
        with self.assertRaises(ValueError):
            road_map.add_road("airport", "beach", -3)
        with self.assertRaises(ValueError):
            road_map.add_road("airport", "beach", 2.5)

    def test_direct_time_in_the_direction_it_was_added(self):
        road_map = example()
        self.assertEqual(road_map.travel_time("airport", "downtown"), 20)
        self.assertEqual(road_map.travel_time("campus", "beach"), 15)

    def test_stops_with_no_road_have_no_travel_time(self):
        road_map = example()
        self.assertIsNone(road_map.travel_time("airport", "island"))
        self.assertEqual(road_map.neighbors("island"), [])

    # def test_roads_are_two_way(self):
    #     road_map = example()
    #     expected = "????"
    #     self.assertEqual(road_map.travel_time("downtown", "airport"), expected)

    # def test_neighbors_include_every_road(self):
    #     road_map = example()
    #     expected = "????"
    #     self.assertEqual(road_map.neighbors("campus"), expected)

    # def test_road_count_counts_each_road_once(self):
    #     road_map = example()
    #     expected = "????"
    #     self.assertEqual(road_map.road_count(), expected)

    # def test_faster_road_wins(self):
    #     road_map = example()
    #     road_map.add_road("airport", "downtown", 30)
    #     expected_after_slower = "????"
    #     self.assertEqual(road_map.travel_time("airport", "downtown"), expected_after_slower)
    #     road_map.add_road("downtown", "airport", 6)
    #     expected_after_faster = "????"
    #     self.assertEqual(road_map.travel_time("airport", "downtown"), expected_after_faster)


if __name__ == "__main__":
    unittest.main()
