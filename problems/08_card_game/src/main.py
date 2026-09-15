"""Runnable demo. Try: python src/main.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck import Deck  # noqa: E402
from hand_data import EXAMPLE_HAND  # noqa: E402
from solver import Solver  # noqa: E402

SHOWCASE = [
    ("straight flush", EXAMPLE_HAND),
    ("flush", "As Ks 9s 4s 2s 7h 3d"),
    ("full house", "Ah Ad Ac 9s 9h 3d 2c"),
    ("wheel straight", "Ah 2c 3d 4s 5h 9c Kd"),
    ("four spades only", "As Ks 9s 4s 7h 2d 3c"),
]


def main():
    print("=== BEGIN card game demo ===")
    deck = Deck()
    solver = Solver(deck)
    print(f"ranks {deck.RANKS}  suits {deck.SUITS}")
    print(f"categories, weakest first: {deck.CATEGORIES}")
    print()
    print(f'parse_card("Ah") -> {deck.parse_card("Ah")}')
    print(f'parse_card("1h") -> {deck.parse_card("1h")}')
    print(f'parse_card("Ax") -> {deck.parse_card("Ax")}')
    print()
    for label, text in SHOWCASE:
        cards = deck.parse_hand(text)
        print(f"{label:18s} {text}")
        print(f"    parsed        {cards}")
        print(f"    flush suit    {deck.flush_suit(cards)}")
        print(f"    straight high {deck.straight_high([rank for rank, _ in cards])}")
        score = solver.best_hand(cards)
        if score is None:
            print("    best hand     not implemented yet")
        else:
            print(f"    best hand     {score} ({deck.category_name(score[0])})")
    print("=== END card game demo ===")


if __name__ == "__main__":
    main()
