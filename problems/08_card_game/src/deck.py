"""Read this first."""

RANKS = "23456789TJQKA"
SUITS = "cdhs"

CATEGORIES = [
    "high card",
    "one pair",
    "two pair",
    "three of a kind",
    "straight",
    "full house",
    "flush",
    "four of a kind",
    "straight flush",
]


class Deck:
    RANKS = RANKS
    SUITS = SUITS
    CATEGORIES = CATEGORIES
    RANK_VALUE = {ch: i + 2 for i, ch in enumerate(RANKS)}

    def parse_card(self, text):
        card = text.strip()
        if len(card) != 2:
            return None
        rank, suit = card[0], card[1]
        if rank not in self.RANK_VALUE:
            return None
        if suit not in self.SUITS:
            return None
        return (self.RANK_VALUE[rank], suit)

    def parse_hand(self, text):
        cards = []
        for piece in text.split():
            card = self.parse_card(piece)
            if card is None:
                raise ValueError(f"not a card: {piece!r}")
            cards.append(card)
        return cards

    def rank_of(self, card):
        return card[0]

    def suit_of(self, card):
        return card[1]

    def category_name(self, category):
        return self.CATEGORIES[category]

    def flush_suit(self, cards):
        counts = {}
        for _rank, suit in cards:
            counts[suit] = counts.get(suit, 0) + 1
        for suit, count in counts.items():
            if count >= 4:
                return suit
        return None

    def straight_high(self, ranks):
        distinct = sorted(set(ranks))
        best = 0
        run = 1
        for i in range(1, len(distinct)):
            if distinct[i] == distinct[i - 1] + 1:
                run += 1
            else:
                run = 1
            if run >= 5:
                best = distinct[i]
        return best
