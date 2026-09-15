import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_parser import LogParser, p95_index  # noqa: E402


class TestP95Index(unittest.TestCase):
    def test_one_value_is_its_own_p95(self):
        self.assertEqual(p95_index(1), 0)

    def test_twenty_values_take_the_second_largest(self):
        self.assertEqual(p95_index(20), 18)

    def test_hundred_values(self):
        self.assertEqual(p95_index(100), 94)

    def test_no_values_is_an_error(self):
        with self.assertRaises(ValueError):
            p95_index(0)


class TestCalendar(unittest.TestCase):
    def setUp(self):
        self.parser = LogParser()

    def test_leap_years(self):
        self.assertTrue(self.parser.is_leap_year(2024))
        self.assertTrue(self.parser.is_leap_year(2000))
        self.assertFalse(self.parser.is_leap_year(1900))
        self.assertFalse(self.parser.is_leap_year(2026))

    def test_days_before_year(self):
        self.assertEqual(self.parser.days_before_year(1970), 0)
        self.assertEqual(self.parser.days_before_year(1971), 365)
        self.assertEqual(self.parser.days_before_year(1973), 1096)

    def test_the_epoch_itself(self):
        self.assertEqual(self.parser.to_epoch("1970-01-01T00:00:00Z"), 0)

    def test_minutes_and_seconds(self):
        self.assertEqual(self.parser.to_epoch("1970-01-01T00:02:05Z"), 125)

    def test_a_whole_day(self):
        self.assertEqual(self.parser.to_epoch("1970-01-02T00:00:00Z"), 86400)

    def test_the_day_after_a_leap_day(self):
        self.assertEqual(self.parser.to_epoch("2024-03-01T00:00:00Z"), 1709251200)

    # def test_an_hour_is_thirty_six_hundred_seconds(self):
    #     expected = "????"
    #     self.assertEqual(self.parser.to_epoch("1970-01-01T02:00:00Z"), expected)

    # def test_a_stamp_late_in_the_day(self):
    #     expected = "????"
    #     self.assertEqual(self.parser.to_epoch("2026-03-01T10:15:32Z"), expected)


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.parser = LogParser()

    def test_a_path_with_no_numbers_is_unchanged(self):
        self.assertEqual(self.parser.endpoint_of("/api/search"), "/api/search")

    def test_a_long_id_collapses(self):
        self.assertEqual(self.parser.endpoint_of("/api/users/4812"), "/api/users/{id}")

    def test_an_id_in_the_middle_collapses(self):
        self.assertEqual(
            self.parser.endpoint_of("/api/orders/4812/items"), "/api/orders/{id}/items"
        )

    def test_a_file_name_is_not_an_id(self):
        self.assertEqual(self.parser.endpoint_of("/static/app.js"), "/static/app.js")

    # def test_a_one_digit_id_is_still_an_id(self):
    #     expected = "????"
    #     self.assertEqual(self.parser.endpoint_of("/api/users/7"), expected)

    # def test_a_two_digit_id_is_still_an_id(self):
    #     expected = "????"
    #     self.assertEqual(self.parser.endpoint_of("/api/cart/42"), expected)


class TestParseLine(unittest.TestCase):
    def setUp(self):
        self.parser = LogParser()

    def test_a_good_line(self):
        row = self.parser.parse_line("2026-03-01T00:15:32Z GET /api/users/1234 200 137")
        self.assertEqual(row[1:], ("GET", "/api/users/1234", 200, 137))

    def test_a_blank_line(self):
        self.assertIsNone(self.parser.parse_line(""))

    def test_too_few_fields(self):
        self.assertIsNone(self.parser.parse_line("2026-03-01T00:15:32Z GET /health 200"))

    def test_an_unknown_method(self):
        self.assertIsNone(self.parser.parse_line("2026-03-01T00:15:32Z PATCH /health 200 4"))

    def test_a_status_that_is_not_a_number(self):
        self.assertIsNone(self.parser.parse_line("2026-03-01T00:15:32Z GET /health ok 4"))


if __name__ == "__main__":
    unittest.main()
