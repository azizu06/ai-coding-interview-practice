"""Middle rung: score the seven cards directly, but work them out from scratch
every time with Counter, sorted and the Deck helpers.

Correct and about twenty times quicker than enumerating five card subsets, but
every hand sorts a set inside Deck.straight_high and builds a Counter, so the
per hand cost stays high and the biggest file runs over budget.
"""

from collections import Counter

from deck import Deck


class Solver:
    def __init__(self, deck: Deck):
        self.deck = deck

    def best_hand(self, cards):
        deck = self.deck
        ranks = sorted((rank for rank, _suit in cards), reverse=True)
        counts = Counter(ranks)
        flush_suit = deck.flush_suit(cards)
        flush_ranks = []
        if flush_suit is not None:
            flush_ranks = sorted(
                (rank for rank, suit in cards if suit == flush_suit), reverse=True
            )
            high = deck.straight_high(flush_ranks)
            if high:
                return (8, (high,))

        quads = sorted((r for r, n in counts.items() if n == 4), reverse=True)
        trips = sorted((r for r, n in counts.items() if n == 3), reverse=True)
        pairs = sorted((r for r, n in counts.items() if n == 2), reverse=True)
        distinct = sorted(counts, reverse=True)

        if quads:
            quad = quads[0]
            kicker = max(r for r in distinct if r != quad)
            return (7, (quad, kicker))

        if flush_suit is not None:
            return (6, tuple(flush_ranks[:5]))

        if trips and (len(trips) > 1 or pairs):
            triple = trips[0]
            partner = max(trips[1:] + pairs[:1])
            return (5, (triple, partner))

        high = deck.straight_high(ranks)
        if high:
            return (4, (high,))

        if trips:
            triple = trips[0]
            kickers = [r for r in distinct if r != triple][:2]
            return (3, (triple, kickers[0], kickers[1]))

        if len(pairs) >= 2:
            high_pair, low_pair = pairs[0], pairs[1]
            kicker = max(r for r in distinct if r not in (high_pair, low_pair))
            return (2, (high_pair, low_pair, kicker))

        if pairs:
            pair = pairs[0]
            kickers = [r for r in distinct if r != pair][:3]
            return (1, (pair, kickers[0], kickers[1], kickers[2]))

        return (0, tuple(distinct[:5]))
