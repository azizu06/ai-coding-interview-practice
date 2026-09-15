import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from request_log import Limit, RequestLog  # noqa: E402
from traffic_data import get_example_limits, get_example_requests  # noqa: E402


def build():
    return RequestLog(get_example_limits(), get_example_requests())


class TestTimestamps(unittest.TestCase):
    def setUp(self):
        self.log = build()

    def test_the_start_of_the_log(self):
        self.assertEqual(self.log.to_millis("0.000"), 0)

    def test_whole_seconds(self):
        self.assertEqual(self.log.to_millis("12.000"), 12000)

    def test_three_digits_of_fraction(self):
        self.assertEqual(self.log.to_millis("12.500"), 12500)

    def test_three_digits_of_a_small_fraction(self):
        self.assertEqual(self.log.to_millis("12.005"), 12005)

    # def test_a_one_digit_fraction_is_tenths(self):
    #     expected = "????"
    #     self.assertEqual(self.log.to_millis("12.5"), expected)

    # def test_a_two_digit_fraction_is_hundredths(self):
    #     expected = "????"
    #     self.assertEqual(self.log.to_millis("3.05"), expected)


class TestParsing(unittest.TestCase):
    def setUp(self):
        self.log = build()

    def test_a_good_request_line(self):
        self.assertEqual(self.log.parse("1.250 c0042 2"), (1250, "c0042", 2))

    def test_a_blank_line(self):
        self.assertIsNone(self.log.parse(""))

    def test_too_many_fields(self):
        self.assertIsNone(self.log.parse("1.250 c0042 2 extra"))

    def test_a_weight_that_is_not_a_number(self):
        self.assertIsNone(self.log.parse("1.250 c0042 heavy"))

    def test_a_good_limit_line(self):
        self.assertEqual(
            self.log.parse_limit("c0042 10000 60 20 8"),
            ("c0042", Limit(10000, 60, 20, 8)),
        )

    def test_a_short_limit_line(self):
        self.assertIsNone(self.log.parse_limit("c0042 10000 60"))


class TestLookups(unittest.TestCase):
    def setUp(self):
        self.log = build()

    def test_clients(self):
        self.assertEqual(self.log.clients(), ["ada", "bob", "cy"])

    def test_requests_are_in_log_order(self):
        senders = [row[1] for row in self.log.requests()]
        self.assertEqual(senders[:4], ["ada", "ada", "ada", "bob"])

    def test_requests_for_a_client(self):
        weights = [row[2] for row in self.log.requests_for("bob")]
        self.assertEqual(weights, [1, 2, 1])

    def test_requests_for_a_client_that_never_appears(self):
        self.assertEqual(self.log.requests_for("nobody"), [])

    def test_a_client_with_its_own_limit(self):
        self.assertEqual(self.log.limit_for("bob"), Limit(2000, 3, 2, 4))

    def test_a_client_falls_back_to_the_default_limit(self):
        self.assertEqual(self.log.limit_for("cy"), Limit(1000, 4, 2, 2))


class TestWindowEdges(unittest.TestCase):
    def setUp(self):
        self.log = build()

    def test_the_arriving_request_is_in_its_own_window(self):
        self.assertTrue(self.log.in_window(1000, 1000, 1000))

    def test_a_recent_request_is_in_the_window(self):
        self.assertTrue(self.log.in_window(600, 1000, 1000))

    def test_the_last_millisecond_of_the_window(self):
        self.assertTrue(self.log.in_window(1, 1000, 1000))

    def test_an_old_request_has_left_the_window(self):
        self.assertFalse(self.log.in_window(0, 1500, 1000))

    # def test_a_request_exactly_one_window_old_has_left(self):
    #     expected = "????"
    #     self.assertEqual(self.log.in_window(0, 1000, 1000), expected)

    # def test_the_far_edge_of_a_wider_window(self):
    #     expected = "????"
    #     self.assertEqual(self.log.in_window(500, 2500, 2000), expected)


class TestRefill(unittest.TestCase):
    def setUp(self):
        self.log = build()
        self.limit = Limit(window_ms=1000, max_weight=4, capacity=3, refill_per_sec=1)

    def test_an_empty_bucket_gains_nothing_in_no_time(self):
        self.assertEqual(self.log.refill(0, 0, self.limit), 0)

    def test_half_a_second_of_refill(self):
        self.assertEqual(self.log.refill(0, 500, self.limit), 500)

    def test_the_bucket_stops_at_capacity(self):
        self.assertEqual(self.log.refill(0, 60000, self.limit), 3000)


if __name__ == "__main__":
    unittest.main()
