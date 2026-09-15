"""Brute force: try all 21 five card subsets of the seven cards, score each one
from scratch, and keep the best.

Cost is 21 full scorings per hand. Correct, easy to believe, and far too slow
once there are more than a few thousand hands.
"""

from collections import Counter
from itertools import combinations

from deck import Deck


class Solver:
    def __init__(self, deck: Deck):
        self.deck = deck

    def score_five(self, five):
        deck = self.deck
        ranks = sorted((rank for rank, _suit in five), reverse=True)
        suits = [suit for _rank, suit in five]
        counts = Counter(ranks)
        is_flush = len(set(suits)) == 1
        high = deck.straight_high(ranks)
        if is_flush and high:
            return (8, (high,))
        groups = sorted(((n, r) for r, n in counts.items()), reverse=True)
        shape = [n for n, _r in groups]
        ordered = [r for _n, r in groups]
        if shape[0] == 4:
            return (7, (ordered[0], ordered[1]))
        if is_flush:
            return (6, tuple(ranks))
        if shape[:2] == [3, 2]:
            return (5, (ordered[0], ordered[1]))
        if high:
            return (4, (high,))
        if shape[0] == 3:
            return (3, (ordered[0], ordered[1], ordered[2]))
        if shape[:2] == [2, 2]:
            return (2, (ordered[0], ordered[1], ordered[2]))
        if shape[0] == 2:
            return (1, (ordered[0], ordered[1], ordered[2], ordered[3]))
        return (0, tuple(ranks))

    def best_hand(self, cards):
        best = None
        for five in combinations(cards, 5):
            score = self.score_five(five)
            if best is None or score > best:
                best = score
        return best
