import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dictionary import Dictionary  # noqa: E402
from solver import Solver  # noqa: E402
from word_files import (  # noqa: E402
    get_distance_two_queries,
    get_example_words,
    get_huge_queries,
    get_large_dictionary,
    get_large_queries,
    get_medium_dictionary,
    get_medium_queries,
    get_small_dictionary,
)


class TestSolverCorrectness(unittest.TestCase):
    def setUp(self):
        self.solver = Solver(Dictionary(get_example_words()))

    def test_exact_word_is_its_own_suggestion(self):
        self.assertIn("apple", self.solver.suggest("apple"))

    def test_one_replacement(self):
        self.assertEqual(self.solver.suggest("grapf"), ["grape", "graph"])

    def test_one_deletion_from_query(self):
        self.assertEqual(self.solver.suggest("breadd"), ["bread"])

    def test_one_insertion_into_query(self):
        self.assertEqual(self.solver.suggest("bred"), ["bread"])

    def test_no_match(self):
        self.assertEqual(self.solver.suggest("zzzzz"), [])

    # def test_query_is_normalized(self):
    #     expected = "????"
    #     self.assertEqual(self.solver.suggest("Grapf!"), expected)

    # def test_result_is_sorted_and_unique(self):
    #     expected = "????"
    #     self.assertEqual(self.solver.suggest("apple"), expected)

    # def test_distance_two(self):
    #     expected = "????"
    #     self.assertEqual(self.solver.suggest("grate", max_distance=2), expected)

    # def test_blank_query_has_no_suggestions(self):
    #     expected = "????"
    #     self.assertEqual(self.solver.suggest("  ! "), expected)

    # def test_small_dictionary(self):
    #     solver = Solver(Dictionary(get_small_dictionary()))
    #     expected = "????"
    #     self.assertEqual(solver.suggest("buvo", max_distance=2), expected)


# Timed tests. Uncomment them for task 6.
# Each one builds the solver, starts a clock, answers every query, and checks the elapsed time.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.medium = Dictionary(get_medium_dictionary())
        cls.large = Dictionary(get_large_dictionary())
        cls.medium_queries = get_medium_queries()
        cls.large_queries = get_large_queries()
        cls.huge_queries = get_huge_queries()
        cls.distance_two_queries = get_distance_two_queries()

    def run_queries(self, dictionary, queries, max_distance):
        solver = Solver(dictionary)
        total = 0
        for query in queries:
            suggestions = solver.suggest(query, max_distance=max_distance)
            self.assertEqual(suggestions, sorted(set(suggestions)))
            for word in suggestions:
                self.assertTrue(dictionary.is_word(word))
            total += len(suggestions)
        return total

    # def test_medium_20_queries(self):
    #     expected_time = 1.0
    #     expected_count = 34
    #     start = time.perf_counter()
    #     total = self.run_queries(self.medium, self.medium_queries, 1)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected_count)
    #     self.assertLess(elapsed, expected_time, f"20 queries: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_300_queries(self):
    #     expected_time = 1.0
    #     expected_count = 572
    #     start = time.perf_counter()
    #     total = self.run_queries(self.large, self.large_queries, 1)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected_count)
    #     self.assertLess(elapsed, expected_time, f"300 queries: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_3000_queries(self):
    #     expected_time = 1.0
    #     expected_count = 6535
    #     start = time.perf_counter()
    #     total = self.run_queries(self.large, self.huge_queries, 1)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected_count)
    #     self.assertLess(elapsed, expected_time, f"3000 queries: {elapsed:.2f}s, need < {expected_time}s")

    # def test_distance_two_200_queries(self):
    #     expected_time = 1.0
    #     expected_count = 973
    #     start = time.perf_counter()
    #     total = self.run_queries(self.medium, self.distance_two_queries, 2)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, expected_count)
    #     self.assertLess(elapsed, expected_time, f"200 queries at distance 2: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
