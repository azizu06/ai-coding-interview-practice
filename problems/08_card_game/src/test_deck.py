import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck import Deck  # noqa: E402


class TestParsing(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_parse_card(self):
        self.assertEqual(self.deck.parse_card("Ah"), (14, "h"))
        self.assertEqual(self.deck.parse_card("2c"), (2, "c"))
        self.assertEqual(self.deck.parse_card("Td"), (10, "d"))

    def test_parse_card_rejects_junk(self):
        self.assertIsNone(self.deck.parse_card("A"))
        self.assertIsNone(self.deck.parse_card("10h"))
        self.assertIsNone(self.deck.parse_card("1h"))
        self.assertIsNone(self.deck.parse_card("Ax"))

    def test_rank_and_suit(self):
        card = self.deck.parse_card("Qs")
        self.assertEqual(self.deck.rank_of(card), 12)
        self.assertEqual(self.deck.suit_of(card), "s")

    def test_parse_hand(self):
        cards = self.deck.parse_hand("Ah Kd 2c")
        self.assertEqual(cards, [(14, "h"), (13, "d"), (2, "c")])

    def test_parse_hand_rejects_junk(self):
        with self.assertRaises(ValueError):
            self.deck.parse_hand("Ah 1z 2c")

    def test_category_name(self):
        self.assertEqual(self.deck.category_name(0), "high card")
        self.assertEqual(self.deck.category_name(6), "flush")
        self.assertEqual(self.deck.category_name(8), "straight flush")


class TestStraights(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_plain_straight(self):
        self.assertEqual(self.deck.straight_high([5, 6, 7, 8, 9]), 9)

    def test_ace_high_straight(self):
        self.assertEqual(self.deck.straight_high([10, 11, 12, 13, 14]), 14)

    def test_no_straight(self):
        self.assertEqual(self.deck.straight_high([2, 3, 4, 5, 7]), 0)

    def test_best_run_in_seven_ranks(self):
        self.assertEqual(self.deck.straight_high([3, 4, 5, 6, 7, 8, 13]), 8)

    def test_duplicates_do_not_make_a_run(self):
        self.assertEqual(self.deck.straight_high([5, 5, 6, 6, 7, 7, 8]), 0)

    # def test_the_wheel_is_a_straight(self):
    #     expected = "????"
    #     self.assertEqual(self.deck.straight_high([14, 2, 3, 4, 5]), expected)

    # def test_the_wheel_inside_seven_ranks(self):
    #     expected = "????"
    #     self.assertEqual(self.deck.straight_high([14, 2, 3, 4, 5, 9, 13]), expected)


class TestFlushes(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_five_of_a_suit(self):
        cards = self.deck.parse_hand("As Ks 9s 4s 2s 7h 3d")
        self.assertEqual(self.deck.flush_suit(cards), "s")

    def test_six_of_a_suit(self):
        cards = self.deck.parse_hand("As Ks 9s 4s 2s 7s 3d")
        self.assertEqual(self.deck.flush_suit(cards), "s")

    def test_two_of_a_suit_is_nothing(self):
        cards = self.deck.parse_hand("As Ks 9h 4h 2c 7c 3d")
        self.assertIsNone(self.deck.flush_suit(cards))

    # def test_four_of_a_suit_is_not_a_flush(self):
    #     cards = self.deck.parse_hand("As Ks 9s 4s 7h 2d 3c")
    #     expected = "????"
    #     self.assertEqual(self.deck.flush_suit(cards), expected)

    # def test_four_and_three_is_still_not_a_flush(self):
    #     cards = self.deck.parse_hand("As Ks 9s 4s 7h 2h 3h")
    #     expected = "????"
    #     self.assertEqual(self.deck.flush_suit(cards), expected)


if __name__ == "__main__":
    unittest.main()
