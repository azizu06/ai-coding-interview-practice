"""Generate the committed hand files. Run: python gen_data.py

Only the small and medium files live on disk. The three big sets used by the
timed tests are rebuilt in memory by src/hand_data.py from the same seeds.

Each line is one seven card hand, cards separated by spaces.
"""

import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
RANKS = "23456789TJQKA"
SUITS = "cdhs"
DECK = [rank + suit for rank in RANKS for suit in SUITS]


def random_hands(count, seed):
    rng = random.Random(seed)
    return [rng.sample(DECK, 7) for _ in range(count)]


def write(name, hands):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(" ".join(hand) for hand in hands) + "\n")
    print(f"{name}: {len(hands)} hands, {os.path.getsize(path)} bytes")


def main():
    write("hands_small.txt", random_hands(100, seed=80001))
    write("hands_medium.txt", random_hands(5000, seed=80002))


if __name__ == "__main__":
    main()
