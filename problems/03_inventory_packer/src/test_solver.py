import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inventory import Inventory  # noqa: E402
from items import (  # noqa: E402
    get_example_items,
    get_huge_items,
    get_large_items,
    get_medium_items,
    get_small_items,
    get_wide_items,
)
from solver import Solver  # noqa: E402


def check_packing(test, boxes, pairs, capacity):
    """Every item exactly once, no box above capacity."""
    weights = dict(pairs)
    packed = [name for box in boxes for name in box]
    test.assertEqual(len(packed), len(weights), "every item must be packed exactly once")
    test.assertEqual(set(packed), set(weights))
    for box in boxes:
        test.assertGreater(len(box), 0, "no empty boxes")
        test.assertLessEqual(sum(weights[name] for name in box), capacity)


class TestSolverCorrectness(unittest.TestCase):
    def test_empty_inventory(self):
        self.assertEqual(Solver(Inventory()).pack(10), [])

    def test_single_item(self):
        self.assertEqual(Solver(Inventory([("anvil", 9)])).pack(10), [["anvil"]])

    def test_two_items_share_a_box(self):
        boxes = Solver(Inventory([("book", 3), ("cup", 3)])).pack(10)
        self.assertEqual(len(boxes), 1)
        self.assertEqual(sorted(boxes[0]), ["book", "cup"])

    def test_item_heavier_than_capacity(self):
        with self.assertRaises(ValueError):
            Solver(Inventory([("piano", 11)])).pack(10)

    def test_packing_is_valid(self):
        pairs = get_example_items()
        boxes = Solver(Inventory(pairs)).pack(10)
        check_packing(self, boxes, pairs, 10)

    # def test_example_box_count(self):
    #     pairs = get_example_items()
    #     boxes = Solver(Inventory(pairs)).pack(10)
    #     check_packing(self, boxes, pairs, 10)
    #     expected_count = "????"
    #     self.assertEqual(len(boxes), expected_count)

    # def test_decreasing_order_matters(self):
    #     pairs = [("a", 4), ("b", 4), ("c", 4), ("d", 6), ("e", 6), ("f", 6)]
    #     boxes = Solver(Inventory(pairs)).pack(10)
    #     check_packing(self, boxes, pairs, 10)
    #     expected_count = "????"
    #     self.assertEqual(len(boxes), expected_count)

    # def test_exact_fit_boxes(self):
    #     pairs = [("a", 5), ("b", 5), ("c", 5), ("d", 5)]
    #     boxes = Solver(Inventory(pairs)).pack(10)
    #     check_packing(self, boxes, pairs, 10)
    #     expected_count = "????"
    #     self.assertEqual(len(boxes), expected_count)

    # def test_small_file(self):
    #     pairs = get_small_items()
    #     boxes = Solver(Inventory(pairs)).pack(10)
    #     check_packing(self, boxes, pairs, 10)
    #     expected_count = "????"
    #     self.assertEqual(len(boxes), expected_count)


# Timed tests. Uncomment them for task 6.
# Each one starts a clock, packs the inventory, and checks the elapsed time and the box count.
# The box count must be at most what first-fit decreasing produces on that file.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.medium_pairs = get_medium_items()
        cls.large_pairs = get_large_items()
        cls.huge_pairs = get_huge_items()
        cls.wide_pairs = get_wide_items()
        cls.medium = Inventory(cls.medium_pairs)
        cls.large = Inventory(cls.large_pairs)
        cls.huge = Inventory(cls.huge_pairs)
        cls.wide = Inventory(cls.wide_pairs)

    # def test_medium_2000_items(self):
    #     expected_time = 1.0
    #     expected_count = "????"
    #     start = time.perf_counter()
    #     boxes = Solver(self.medium).pack(100)
    #     elapsed = time.perf_counter() - start
    #     check_packing(self, boxes, self.medium_pairs, 100)
    #     self.assertLessEqual(len(boxes), expected_count)
    #     self.assertLess(elapsed, expected_time, f"2000 items: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_40000_items(self):
    #     expected_time = 1.0
    #     expected_count = "????"
    #     start = time.perf_counter()
    #     boxes = Solver(self.large).pack(100)
    #     elapsed = time.perf_counter() - start
    #     check_packing(self, boxes, self.large_pairs, 100)
    #     self.assertLessEqual(len(boxes), expected_count)
    #     self.assertLess(elapsed, expected_time, f"40000 items: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_200000_items(self):
    #     expected_time = 1.0
    #     expected_count = "????"
    #     start = time.perf_counter()
    #     boxes = Solver(self.huge).pack(100)
    #     elapsed = time.perf_counter() - start
    #     check_packing(self, boxes, self.huge_pairs, 100)
    #     self.assertLessEqual(len(boxes), expected_count)
    #     self.assertLess(elapsed, expected_time, f"200000 items: {elapsed:.2f}s, need < {expected_time}s")

    # def test_wide_weights_20000_items(self):
    #     expected_time = 1.0
    #     expected_count = "????"
    #     start = time.perf_counter()
    #     boxes = Solver(self.wide).pack(100000)
    #     elapsed = time.perf_counter() - start
    #     check_packing(self, boxes, self.wide_pairs, 100000)
    #     self.assertLessEqual(len(boxes), expected_count)
    #     self.assertLess(elapsed, expected_time, f"20000 wide items: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
