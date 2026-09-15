"""Loaders for the dictionaries and query lists in ../data."""

import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def _read(name, keep_spaces=False):
    path = os.path.join(DATA_DIR, name)
    with open(path, encoding="utf-8") as handle:
        lines = [line.rstrip("\n") for line in handle]
    if keep_spaces:
        return [line for line in lines if line.strip()]
    return [line.strip() for line in lines if line.strip()]


def get_example_words():
    """The tiny dictionary used in README.md and main.py."""
    return ["apple", "apply", "ample", "maple", "grape", "graph", "great", "treat", "tread", "bread"]


def get_small_dictionary():
    return _read("dictionary_small.txt")


def get_medium_dictionary():
    return _read("dictionary_medium.txt")


def get_large_dictionary():
    return _read("dictionary_large.txt")


def get_medium_queries():
    return _read("queries_medium.txt", keep_spaces=True)


def get_large_queries():
    return _read("queries_large.txt", keep_spaces=True)


def get_huge_queries():
    return _read("queries_huge.txt", keep_spaces=True)


def get_distance_two_queries():
    """Queries that are up to two edits away from a word in the medium dictionary."""
    return _read("queries_distance_two.txt", keep_spaces=True)
