import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_data import (  # noqa: E402
    get_example_lines,
    get_large_lines,
    get_medium_lines,
    get_small_lines,
    get_wide_lines,
)
from log_parser import LogParser  # noqa: E402
from solver import Solver  # noqa: E402

PARSER = LogParser()

TINY_LOG = [
    "2026-03-01T00:00:00Z GET /a 200 10",
    "2026-03-01T00:00:30Z GET /a 200 90",
    "2026-03-01T00:05:00Z GET /b 200 50",
]


def scan(lines, width, step, k):
    return Solver(PARSER, lines).scan_windows(width, step, k)


def p95_total(lines, width, step, k):
    """Sum of every p95 the scan reports. A cheap whole log checksum."""
    total = 0
    for window in Solver(PARSER, lines).scan_windows(width, step, k):
        for _endpoint, value in window:
            total += value
    return total


class TestSolverCorrectness(unittest.TestCase):
    def test_one_minute_windows(self):
        self.assertEqual(
            scan(get_example_lines(), 60, 60, 3),
            [
                [("/api/search", 900), ("/api/orders/{id}", 120), ("/api/users/{id}", 60)],
                [("/api/orders/{id}", 400), ("/api/search", 100), ("/api/users/{id}", 55)],
                [("/api/search", 1500)],
            ],
        )

    def test_one_window_over_the_whole_log(self):
        self.assertEqual(
            scan(get_example_lines(), 600, 600, 5),
            [
                [
                    ("/api/search", 1500),
                    ("/api/orders/{id}", 400),
                    ("/api/users/{id}", 60),
                    ("/health", 3),
                ]
            ],
        )

    def test_k_truncates_each_window(self):
        windows = scan(get_example_lines(), 600, 600, 2)
        self.assertEqual(windows, [[("/api/search", 1500), ("/api/orders/{id}", 400)]])

    def test_a_window_holds_a_single_request(self):
        self.assertEqual(scan(TINY_LOG[:1], 60, 60, 3), [[("/a", 10)]])

    # def test_an_empty_log_has_no_windows(self):
    #     expected = "????"
    #     self.assertEqual(scan([], 60, 60, 3), expected)

    # def test_windows_with_no_requests_stay_in_the_result(self):
    #     expected = "????"
    #     self.assertEqual(scan(TINY_LOG, 60, 60, 2), expected)

    # def test_overlapping_windows_share_requests(self):
    #     expected = "????"
    #     self.assertEqual(scan(get_example_lines(), 120, 60, 2), expected)


# Timed tests. Uncomment them for task 6.
# Each one scans a whole log and checks the summed p95 values.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.small = get_small_lines()
        cls.medium = get_medium_lines()
        cls.large = get_large_lines()
        cls.wide = get_wide_lines()

    # def test_small_2000_requests(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = p95_total(self.small, 120, 30, 3)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 85171)
    #     self.assertLess(elapsed, expected_time, f"2000 requests: {elapsed:.2f}s, need < {expected_time}s")

    # def test_medium_15000_requests(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = p95_total(self.medium, 300, 60, 5)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 315690)
    #     self.assertLess(elapsed, expected_time, f"15000 requests: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_200000_requests(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = p95_total(self.large, 300, 15, 5)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 5115470)
    #     self.assertLess(elapsed, expected_time, f"960 windows: {elapsed:.2f}s, need < {expected_time}s")

    # def test_wide_1440_overlapping_windows(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = p95_total(self.wide, 900, 5, 5)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 7679811)
    #     self.assertLess(elapsed, expected_time, f"1440 wide windows: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
