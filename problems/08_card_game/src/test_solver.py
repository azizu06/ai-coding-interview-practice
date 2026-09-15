import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck import Deck  # noqa: E402
from hand_data import (  # noqa: E402
    EXAMPLE_HAND,
    get_huge_hands,
    get_large_hands,
    get_medium_hands,
    get_rich_hands,
    get_small_hands,
)
from solver import Solver  # noqa: E402

DECK = Deck()


def score(text):
    return Solver(DECK).best_hand(DECK.parse_hand(text))


def category_total(hands):
    """Sum of the category number of every hand. A cheap whole file checksum."""
    solver = Solver(DECK)
    total = 0
    for hand in hands:
        total += solver.best_hand(hand)[0]
    return total


class TestSolverCorrectness(unittest.TestCase):
    def test_high_card(self):
        self.assertEqual(score("Ah Kd 9c 7s 4h 3d 2c"), (0, (14, 13, 9, 7, 4)))

    def test_one_pair(self):
        self.assertEqual(score("Ah Ad 9c 7s 4h 3d 2c"), (1, (14, 9, 7, 4)))

    def test_two_pair(self):
        self.assertEqual(score("Ah Ad 9c 9s 4h 3d 2c"), (2, (14, 9, 4)))

    def test_three_of_a_kind(self):
        self.assertEqual(score("Ah Ad Ac 9s 4h 3d 2c"), (3, (14, 9, 4)))

    def test_straight(self):
        self.assertEqual(score("5h 6d 7c 8s 9h Kd 2c"), (4, (9,)))

    def test_four_of_a_kind(self):
        self.assertEqual(score("Ah Ad Ac As 9h 3d 2c"), (7, (14, 9)))

    def test_straight_flush(self):
        self.assertEqual(score(EXAMPLE_HAND), (8, (13,)))

    # def test_the_wheel_counts_as_a_straight(self):
    #     expected = "????"
    #     self.assertEqual(score("Ah 2c 3d 4s 5h 9c Kd"), expected)

    # def test_flush(self):
    #     expected = "????"
    #     self.assertEqual(score("As Ks 9s 4s 2s 7h 3d"), expected)

    # def test_six_of_a_suit_keeps_the_best_five(self):
    #     expected = "????"
    #     self.assertEqual(score("As Ks 9s 4s 2s 7s 3d"), expected)

    # def test_four_of_a_suit_is_only_a_high_card(self):
    #     expected = "????"
    #     self.assertEqual(score("As Ks 9s 4s 7h 2d 3c"), expected)

    # def test_two_triples_make_a_full_house(self):
    #     expected = "????"
    #     self.assertEqual(score("9h 9c 9d 5s 5h 5c 2d"), expected)

    # def test_house_rule_a_flush_beats_a_full_house(self):
    #     flush = score("As Ks 9s 4s 2s 7h 3d")
    #     full_house = score("Ah Ad Ac 9s 9h 3d 2c")
    #     expected = "????"
    #     self.assertEqual(flush > full_house, expected)


# Timed tests. Uncomment them for task 6.
# Each one scores every hand in a file and checks the summed category numbers.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.small = get_small_hands()
        cls.medium = get_medium_hands()
        cls.large = get_large_hands()
        cls.rich = get_rich_hands()
        cls.huge = get_huge_hands()

    # def test_small_100_hands(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = category_total(self.small)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 141)
    #     self.assertLess(elapsed, expected_time, f"100 hands: {elapsed:.2f}s, need < {expected_time}s")

    # def test_medium_5000_hands(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = category_total(self.medium)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 7797)
    #     self.assertLess(elapsed, expected_time, f"5000 hands: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_60000_hands(self):
    #     expected_time = 1.5
    #     start = time.perf_counter()
    #     total = category_total(self.large)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 94159)
    #     self.assertLess(elapsed, expected_time, f"60000 hands: {elapsed:.2f}s, need < {expected_time}s")

    # def test_rich_60000_flushy_hands(self):
    #     expected_time = 1.5
    #     start = time.perf_counter()
    #     total = category_total(self.rich)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 240635)
    #     self.assertLess(elapsed, expected_time, f"60000 flushy hands: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_250000_hands(self):
    #     expected_time = 1.5
    #     start = time.perf_counter()
    #     total = category_total(self.huge)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 391130)
    #     self.assertLess(elapsed, expected_time, f"250000 hands: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
