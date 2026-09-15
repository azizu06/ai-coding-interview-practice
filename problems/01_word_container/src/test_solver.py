import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver import Solver  # noqa: E402
from word_list import WordList  # noqa: E402
from words import (  # noqa: E402
    get_example_words,
    get_huge_words,
    get_large_words,
    get_long_words,
    get_medium_words,
    get_small_words,
)


def solve(words):
    return Solver(WordList(words)).find_container_words()


class TestSolverCorrectness(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(solve([]), [])

    def test_single_word(self):
        self.assertEqual(solve(["alone"]), [])

    def test_no_containment(self):
        self.assertEqual(solve(["cat", "dog", "bird"]), [])

    def test_one_container(self):
        self.assertEqual(solve(["cat", "concatenate", "dog"]), ["concatenate"])

    def test_result_is_sorted(self):
        self.assertEqual(solve(["hotdog", "dog", "concatenate", "cat"]), ["concatenate", "hotdog"])

    # def test_example_words(self):
    #     expected = "????"
    #     self.assertEqual(solve(get_example_words()), expected)

    # def test_word_containing_two_others_is_listed_once(self):
    #     expected = "????"
    #     self.assertEqual(solve(["sun", "hat", "sunhat", "sunhats"]), expected)

    # def test_prefix_and_suffix_both_count(self):
    #     expected = "????"
    #     self.assertEqual(solve(["ten", "tenor", "often", "of"]), expected)

    # def test_duplicate_input_word_is_not_its_own_container(self):
    #     expected = "????"
    #     self.assertEqual(solve(["dog", "dog", "cat"]), expected)

    # def test_small_file(self):
    #     expected_count = "????"
    #     self.assertEqual(len(solve(get_small_words())), expected_count)


# Timed tests. Uncomment them for task 6.
# Each one loads its words, starts a clock, runs the solver, and checks the elapsed time.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.medium = WordList(get_medium_words())
        cls.large = WordList(get_large_words())
        cls.huge = WordList(get_huge_words())
        cls.long = WordList(get_long_words())

    def check_result(self, result, word_list):
        self.assertEqual(result, sorted(set(result)))
        known = set(word_list.words())
        for word in result:
            self.assertIn(word, known)

    # def test_medium_500_words(self):
    #     expected_time = 1.0
    #     expected_count = 73
    #     start = time.perf_counter()
    #     result = Solver(self.medium).find_container_words()
    #     elapsed = time.perf_counter() - start
    #     self.check_result(result, self.medium)
    #     self.assertEqual(len(result), expected_count)
    #     self.assertLess(elapsed, expected_time, f"500 words: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_10000_words(self):
    #     expected_time = 0.5
    #     expected_count = 1567
    #     start = time.perf_counter()
    #     result = Solver(self.large).find_container_words()
    #     elapsed = time.perf_counter() - start
    #     self.check_result(result, self.large)
    #     self.assertEqual(len(result), expected_count)
    #     self.assertLess(elapsed, expected_time, f"10000 words: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_25000_words(self):
    #     expected_time = 1.0
    #     expected_count = 4305
    #     start = time.perf_counter()
    #     result = Solver(self.huge).find_container_words()
    #     elapsed = time.perf_counter() - start
    #     self.check_result(result, self.huge)
    #     self.assertEqual(len(result), expected_count)
    #     self.assertLess(elapsed, expected_time, f"25000 words: {elapsed:.2f}s, need < {expected_time}s")

    # def test_long_words(self):
    #     expected_time = 1.0
    #     expected_count = 6
    #     start = time.perf_counter()
    #     result = Solver(self.long).find_container_words()
    #     elapsed = time.perf_counter() - start
    #     self.check_result(result, self.long)
    #     self.assertEqual(len(result), expected_count)
    #     self.assertLess(elapsed, expected_time, f"30 long words: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
