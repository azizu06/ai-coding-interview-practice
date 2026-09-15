"""Reference solution.

Two ideas do the work:

  * score the seven cards straight away instead of trying all 21 five card
    subsets; rank counts and a flush count already say which category the best
    five cards form
  * look straights up in a table indexed by the 13 bit mask of which ranks are
    present, built once, so the hot loop never sorts anything
"""

from deck import Deck


class Solver:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.straight_table = self._build_straight_table()

    def _build_straight_table(self):
        """straight_table[mask] is the high card of the best straight in mask."""
        table = [0] * (1 << 15)
        for mask in range(1 << 13):
            ranks = [r for r in range(2, 15) if mask & (1 << (r - 2))]
            table[sum(1 << r for r in ranks)] = self.deck.straight_high(ranks)
        return table

    def best_hand(self, cards):
        counts = [0] * 15
        suit_counts = {}
        mask = 0
        for rank, suit in cards:
            counts[rank] += 1
            mask |= 1 << rank
            suit_counts[suit] = suit_counts.get(suit, 0) + 1

        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break

        if flush_suit is not None:
            flush_ranks = sorted(
                (rank for rank, suit in cards if suit == flush_suit), reverse=True
            )
            flush_mask = 0
            for rank in flush_ranks:
                flush_mask |= 1 << rank
            high = self.straight_table[flush_mask]
            if high:
                return (8, (high,))

        quad = 0
        trips = []
        pairs = []
        for rank in range(14, 1, -1):
            count = counts[rank]
            if count == 4:
                if not quad:
                    quad = rank
            elif count == 3:
                trips.append(rank)
            elif count == 2:
                pairs.append(rank)

        if quad:
            kicker = max(r for r in range(14, 1, -1) if counts[r] and r != quad)
            return (7, (quad, kicker))

        if flush_suit is not None:
            return (6, tuple(flush_ranks[:5]))

        if trips and (len(trips) > 1 or pairs):
            triple = trips[0]
            partner = trips[1] if len(trips) > 1 else 0
            if pairs and pairs[0] > partner:
                partner = pairs[0]
            return (5, (triple, partner))

        high = self.straight_table[mask]
        if high:
            return (4, (high,))

        present = [r for r in range(14, 1, -1) if counts[r]]
        if trips:
            triple = trips[0]
            kickers = [r for r in present if r != triple][:2]
            return (3, (triple, kickers[0], kickers[1]))

        if len(pairs) >= 2:
            high_pair, low_pair = pairs[0], pairs[1]
            kicker = next(r for r in present if r != high_pair and r != low_pair)
            return (2, (high_pair, low_pair, kicker))

        if pairs:
            pair = pairs[0]
            kickers = [r for r in present if r != pair][:3]
            return (1, (pair, kickers[0], kickers[1], kickers[2]))

        return (0, tuple(present[:5]))
