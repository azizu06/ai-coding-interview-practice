"""Generate the dictionary and query files for the Spell Checker problem.

Run from this directory: python gen_data.py
Words are made of consonant-vowel syllables so they look pronounceable and rarely collide.
"""

import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
CONSONANTS = "bcdfghjklmnprstvwz"
VOWELS = "aeiou"
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def make_word(rng):
    syllables = rng.randint(2, 5)
    word = ""
    for _ in range(syllables):
        word += rng.choice(CONSONANTS) + rng.choice(VOWELS)
        if rng.random() < 0.3:
            word += rng.choice(CONSONANTS)
    return word[:12]


def build_dictionary(rng, count):
    seen = set()
    words = []
    while len(words) < count:
        word = make_word(rng)
        if word in seen:
            continue
        seen.add(word)
        words.append(word)
    return sorted(words)


def mutate(rng, word, edits):
    for _ in range(edits):
        kind = rng.choice("ids")
        if kind == "i":
            i = rng.randrange(len(word) + 1)
            word = word[:i] + rng.choice(LETTERS) + word[i:]
        elif kind == "d" and len(word) > 2:
            i = rng.randrange(len(word))
            word = word[:i] + word[i + 1:]
        else:
            i = rng.randrange(len(word))
            word = word[:i] + rng.choice(LETTERS) + word[i + 1:]
    return word


def decorate(rng, word):
    """Add the kind of noise real text has: capitals and trailing punctuation."""
    roll = rng.random()
    if roll < 0.1:
        word = word.capitalize()
    elif roll < 0.15:
        word = word.upper()
    if rng.random() < 0.15:
        word += rng.choice([".", ",", "!", "?"])
    if rng.random() < 0.05:
        word = " " + word + " "
    return word


def build_queries(rng, dictionary, count, edits):
    queries = []
    for _ in range(count):
        roll = rng.random()
        base = rng.choice(dictionary)
        if roll < 0.75:
            query = mutate(rng, base, edits)
        elif roll < 0.9:
            query = base
        else:
            query = "".join(rng.choice(LETTERS) for _ in range(rng.randint(4, 9)))
        queries.append(decorate(rng, query))
    return queries


def write(name, lines):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"{name}: {len(lines)} lines, {os.path.getsize(path)} bytes")


def main():
    rng = random.Random(20260902)
    small = build_dictionary(rng, 100)
    medium = build_dictionary(rng, 5000)
    large = build_dictionary(rng, 50000)
    write("dictionary_small.txt", small)
    write("dictionary_medium.txt", medium)
    write("dictionary_large.txt", large)
    write("queries_medium.txt", build_queries(rng, medium, 20, 1))
    write("queries_large.txt", build_queries(rng, large, 300, 1))
    write("queries_huge.txt", build_queries(rng, large, 3000, 1))
    write("queries_distance_two.txt", build_queries(rng, medium, 200, 2))


if __name__ == "__main__":
    main()
