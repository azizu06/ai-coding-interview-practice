"""Loaders for the word files in ../data."""

import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def _read(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def get_example_words():
    """The tiny list used in INSTRUCTIONS.md and main.py."""
    return ["cat", "concatenate", "dog", "hotdog", "sun", "sunny", "ate", "plate", "ten"]


def get_small_words():
    return _read("words_small.txt")


def get_medium_words():
    return _read("words_medium.txt")


def get_large_words():
    return _read("words_large.txt")


def get_huge_words():
    return _read("words_huge.txt")


def get_long_words():
    """Thirty words, most of them about a thousand letters long."""
    return _read("words_long.txt")
