import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from request_log import RequestLog  # noqa: E402
from solver import Solver  # noqa: E402
from traffic_data import (  # noqa: E402
    get_example_limits,
    get_example_requests,
    get_hot_limits,
    get_hot_requests,
    get_large_limits,
    get_large_requests,
    get_medium_limits,
    get_medium_requests,
    get_small_limits,
    get_small_requests,
)

# ada has a window of 1000 ms holding weight 4, and a bucket of 3 units that
# regains 1 unit per second.
EDGE_REQUESTS = [
    "0.0 ada 2",
    "0.1 ada 1",
    "0.2 ada 1",
    "1.0 ada 1",
]


def decide(request_lines, limit_lines=None):
    limits = get_example_limits() if limit_lines is None else limit_lines
    return Solver(RequestLog(limits, request_lines)).decide()


def allowed_count(limit_lines, request_lines):
    """How many requests the limiter lets through. A whole log checksum."""
    return sum(Solver(RequestLog(limit_lines, request_lines)).decide())


class TestSolverCorrectness(unittest.TestCase):
    def test_a_single_request_is_allowed(self):
        self.assertEqual(decide(["0.0 ada 1"]), [True])

    def test_a_full_bucket_runs_out(self):
        self.assertEqual(
            decide(["0.0 ada 1", "0.01 ada 1", "0.02 ada 1", "0.03 ada 1"]),
            [True, True, True, False],
        )

    def test_a_denied_request_spends_nothing(self):
        # The weight 3 request is turned away, so the bucket still holds enough
        # for the weight 1 request right behind it.
        self.assertEqual(decide(["0.0 cy 3", "0.01 cy 1"]), [False, True])

    def test_clients_do_not_share_a_bucket(self):
        self.assertEqual(
            decide(["0.0 ada 1", "0.001 bob 1", "0.002 cy 1"]),
            [True, True, True],
        )

    def test_waiting_refills_the_bucket(self):
        self.assertEqual(
            decide(["0.0 cy 2", "0.01 cy 1", "5.0 cy 2"]),
            [True, False, True],
        )

    # def test_an_empty_log_decides_nothing(self):
    #     expected = "????"
    #     self.assertEqual(decide([]), expected)

    # def test_the_far_edge_of_the_window(self):
    #     expected = "????"
    #     self.assertEqual(decide(EDGE_REQUESTS), expected)

    # def test_the_two_rules_interact(self):
    #     # ada's last request has a token waiting for it, but too many
    #     # requests inside the window.
    #     expected = "????"
    #     self.assertEqual(decide(get_example_requests()), expected)


# Timed tests. Uncomment them for task 6.
# Each one decides a whole log and checks how many requests were allowed.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.small = (get_small_limits(), get_small_requests())
        cls.medium = (get_medium_limits(), get_medium_requests())
        cls.large = (get_large_limits(), get_large_requests())
        cls.hot = (get_hot_limits(), get_hot_requests())

    # def test_small_4000_requests(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = allowed_count(*self.small)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 3356)
    #     self.assertLess(elapsed, expected_time, f"4000 requests: {elapsed:.2f}s, need < {expected_time}s")

    # def test_medium_40000_requests(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = allowed_count(*self.medium)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 33873)
    #     self.assertLess(elapsed, expected_time, f"40000 requests: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_300000_requests(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = allowed_count(*self.large)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 257015)
    #     self.assertLess(elapsed, expected_time, f"300000 requests: {elapsed:.2f}s, need < {expected_time}s")

    # def test_hot_eight_very_busy_clients(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = allowed_count(*self.hot)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 67971)
    #     self.assertLess(elapsed, expected_time, f"8 busy clients: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
