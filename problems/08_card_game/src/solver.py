"""You'll implement this."""

from deck import Deck


class Solver:
    def __init__(self, deck: Deck):
        self.deck = deck

    def best_hand(self, cards):
        """Score the best five card hand inside a seven card hand.

        `cards` is a list of parsed cards, each a (rank, suit) pair.
        Return (category, tiebreakers) as described in deck.py, where
        `category` is an int from 0 to 8 and `tiebreakers` is a tuple.

        Example: five spades and two other cards score as a flush, which in
        this game outranks a full house.
        """
        pass
