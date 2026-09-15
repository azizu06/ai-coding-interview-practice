"""Loaders for the seven card hands.

The small and medium files are committed under ../data and are read through
Deck.parse_hand. The three big sets would be megabytes of text, so they are
built here from fixed seeds as parsed (rank, suit) cards.

    get_example_hand()   the hand used in INSTRUCTIONS.md and main.py
    get_small_hands()    100 hands from a shuffled 52 card deck
    get_medium_hands()   5000 hands from a shuffled 52 card deck
    get_large_hands()    60000 hands from a shuffled 52 card deck
    get_huge_hands()     250000 hands from a shuffled 52 card deck
    get_rich_hands()     60000 hands rigged so flushes and straights are common
"""

import os
import random

from deck import Deck

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

EXAMPLE_HAND = "Ks Qs Js Ts 9s Kd Kc"

_DECK = [(rank, suit) for rank in range(2, 15) for suit in "cdhs"]
_BY_SUIT = {suit: [(rank, suit) for rank in range(2, 15)] for suit in "cdhs"}
_CACHE = {}


def _read(name):
    deck = Deck()
    path = os.path.join(DATA_DIR, name)
    with open(path, encoding="utf-8") as handle:
        return [deck.parse_hand(line) for line in handle if line.strip()]


def _random_hands(count, seed):
    rng = random.Random(seed)
    sample = rng.sample
    deck = _DECK
    return [sample(deck, 7) for _ in range(count)]


def _rich_hands(count, seed):
    rng = random.Random(seed)
    hands = []
    for _ in range(count):
        roll = rng.random()
        if roll < 0.35:
            suit = rng.choice("cdhs")
            hand = rng.sample(_BY_SUIT[suit], 5)
            taken = set(hand)
            hand += rng.sample([c for c in _DECK if c not in taken], 2)
        elif roll < 0.70:
            low = rng.randint(2, 10)
            hand = [(low + step, rng.choice("cdhs")) for step in range(5)]
            taken = set(hand)
            hand += rng.sample([c for c in _DECK if c not in taken], 2)
        else:
            hand = rng.sample(_DECK, 7)
        hands.append(hand)
    return hands


def _cached(key, factory):
    if key not in _CACHE:
        _CACHE[key] = factory()
    return _CACHE[key]


def get_example_hand():
    return Deck().parse_hand(EXAMPLE_HAND)


def get_small_hands():
    return _cached("small", lambda: _read("hands_small.txt"))


def get_medium_hands():
    return _cached("medium", lambda: _read("hands_medium.txt"))


def get_large_hands():
    return _cached("large", lambda: _random_hands(60000, seed=80003))


def get_huge_hands():
    return _cached("huge", lambda: _random_hands(250000, seed=80004))


def get_rich_hands():
    return _cached("rich", lambda: _rich_hands(60000, seed=80005))
