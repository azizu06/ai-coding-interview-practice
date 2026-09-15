"""Middle rung: still enumerate all 21 five card subsets, but score each subset
with a fast table driven scorer instead of Counter and sorted.

This is the tempting first move after brute force: the scorer looked slow, so
make the scorer quicker. It is about three times faster than brute force and
still twenty one times more work than it needs to be, because the seven cards
already say which five are best.
"""

from itertools import combinations

from deck import Deck


class Solver:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.straight_table = [0] * (1 << 15)
        for mask in range(1 << 13):
            ranks = [r for r in range(2, 15) if mask & (1 << (r - 2))]
            self.straight_table[sum(1 << r for r in ranks)] = deck.straight_high(ranks)

    def score_five(self, five):
        counts = [0] * 15
        mask = 0
        suit = five[0][1]
        is_flush = True
        for rank, card_suit in five:
            counts[rank] += 1
            mask |= 1 << rank
            if card_suit != suit:
                is_flush = False
        high = self.straight_table[mask]
        if is_flush and high:
            return (8, (high,))
        groups = sorted(((counts[r], r) for r in range(2, 15) if counts[r]), reverse=True)
        shape = groups[0][0]
        ordered = [r for _n, r in groups]
        if shape == 4:
            return (7, (ordered[0], ordered[1]))
        if is_flush:
            return (6, tuple(ordered))
        if shape == 3 and groups[1][0] == 2:
            return (5, (ordered[0], ordered[1]))
        if high:
            return (4, (high,))
        if shape == 3:
            return (3, (ordered[0], ordered[1], ordered[2]))
        if shape == 2 and groups[1][0] == 2:
            return (2, (ordered[0], ordered[1], ordered[2]))
        if shape == 2:
            return (1, (ordered[0], ordered[1], ordered[2], ordered[3]))
        return (0, tuple(ordered))

    def best_hand(self, cards):
        best = None
        for five in combinations(cards, 5):
            score = self.score_five(five)
            if best is None or score > best:
                best = score
        return best
