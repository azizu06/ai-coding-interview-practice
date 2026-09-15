"""Generate the word files for the Word Container problem.

Run from this directory: python gen_data.py
Every file is deterministic for a given seed, so re-running rewrites the same content.
"""

import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def random_word(rng, low, high):
    return "".join(rng.choice(LETTERS) for _ in range(rng.randint(low, high)))


def build_words(rng, count, low, high, planted_share):
    """Random words plus a share of words that wrap an earlier word in extra letters."""
    words = []
    seen = set()
    while len(words) < count:
        if words and rng.random() < planted_share:
            inner = rng.choice(words)
            left = random_word(rng, 0, 3)
            right = random_word(rng, 0, 3)
            if not left and not right:
                left = rng.choice(LETTERS)
            candidate = left + inner + right
        else:
            candidate = random_word(rng, low, high)
        if candidate in seen:
            continue
        seen.add(candidate)
        words.append(candidate)
    rng.shuffle(words)
    return words


def build_long_words(rng):
    """Thirty words, most of them well over a thousand letters. Six of them wrap one of the shorter ones."""
    short = [random_word(rng, 300, 500) for _ in range(10)]
    long_words = [random_word(rng, 1700, 1999) for _ in range(14)]
    wrapped = []
    for inner in short[:6]:
        left = random_word(rng, 200, 400)
        right = random_word(rng, 200, 400)
        wrapped.append(left + inner + right)
    words = short + long_words + wrapped
    rng.shuffle(words)
    return words


def write(name, words):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(words) + "\n")
    print(f"{name}: {len(words)} words, {os.path.getsize(path)} bytes")


def main():
    rng = random.Random(20260914)
    write("words_small.txt", build_words(rng, 20, 3, 7, 0.3))
    write("words_medium.txt", build_words(rng, 500, 4, 10, 0.15))
    write("words_large.txt", build_words(rng, 10000, 4, 10, 0.15))
    write("words_huge.txt", build_words(rng, 25000, 4, 10, 0.15))
    write("words_long.txt", build_long_words(rng))


if __name__ == "__main__":
    main()
