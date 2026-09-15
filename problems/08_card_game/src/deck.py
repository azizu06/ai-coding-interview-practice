"""Read this first.

This file holds the rules of the card game and the code that reads cards.

A card is two characters: a rank then a suit.

    ranks   2 3 4 5 6 7 8 9 T J Q K A   (T is the ten, A is high)
    suits   c d h s                     (clubs diamonds hearts spades)

So "Ah" is the ace of hearts and "Td" is the ten of diamonds. Suits have no
strength of their own; they only decide flushes.

A player holds seven cards and scores the best five of them. The categories,
weakest first, are:

    0  high card
    1  one pair
    2  two pair
    3  three of a kind
    4  straight
    5  full house
    6  flush
    7  four of a kind
    8  straight flush

Note the house rule: in this game a FLUSH BEATS A FULL HOUSE. That is not how
most poker variants score, so do not trust a memorised table.

A straight is five ranks in a row. The ace plays both high (T J Q K A) and low
(A 2 3 4 5). The low one is called the wheel and its high card counts as 5, so
it is the weakest straight.

A hand score is a pair (category, tiebreakers). Tiebreakers are compared left
to right, so plain tuple comparison ranks two scores correctly.

    high card        five ranks, highest first
    one pair         the pair rank, then three kickers highest first
    two pair         higher pair, lower pair, kicker
    three of a kind  the triple rank, then two kickers highest first
    straight         the high card of the run
    full house       the triple rank, then the pair rank
    flush            five ranks of the flush suit, highest first
    four of a kind   the quad rank, then the kicker
    straight flush   the high card of the run
"""

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
        """Turn "Ah" into (14, "h"). Return None when the text is not a card."""
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
        """Parse a whitespace separated line of cards. Raises on a bad card."""
        cards = []
        for piece in text.split():
            card = self.parse_card(piece)
            if card is None:
                raise ValueError(f"not a card: {piece!r}")
            cards.append(card)
        return cards

    def rank_of(self, card):
        """The rank value of a parsed card."""
        return card[0]

    def suit_of(self, card):
        """The suit letter of a parsed card."""
        return card[1]

    def category_name(self, category):
        """The printable name of a category number."""
        return self.CATEGORIES[category]

    def flush_suit(self, cards):
        """The suit that appears five or more times, or None."""
        counts = {}
        for _rank, suit in cards:
            counts[suit] = counts.get(suit, 0) + 1
        for suit, count in counts.items():
            if count >= 4:
                return suit
        return None

    def straight_high(self, ranks):
        """The high card of the best straight inside `ranks`, or 0 for none.

        `ranks` is any collection of rank values. Duplicates are ignored. The
        wheel A 2 3 4 5 counts as a straight whose high card is 5.
        """
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
