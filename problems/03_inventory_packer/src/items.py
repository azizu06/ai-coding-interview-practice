"""Loaders for the item files in ../data, plus the generator for the huge set.

The huge set (200000 items) would be a 2 MB file, so it is generated in memory from a
fixed seed instead. `generate_items` is also what data/gen_data.py uses for the files.
"""

import os
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def generate_items(count, low, high, seed, prefix="item"):
    """Deterministic list of (name, weight) pairs with integer weights in [low, high]."""
    rng = random.Random(seed)
    width = len(str(count))
    return [(f"{prefix}{i:0{width}d}", rng.randint(low, high)) for i in range(1, count + 1)]


def _read(name):
    path = os.path.join(DATA_DIR, name)
    items = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            item_name, weight = line.split()
            items.append((item_name, int(weight)))
    return items


def get_example_items():
    """The tiny set used in INSTRUCTIONS.md and main.py."""
    return [("anvil", 9), ("book", 3), ("cup", 3), ("dish", 4), ("egg", 1), ("fan", 6), ("globe", 5)]


def get_small_items():
    return _read("items_small.txt")


def get_medium_items():
    return _read("items_medium.txt")


def get_large_items():
    return _read("items_large.txt")


def get_wide_items():
    """20000 items whose weights span 1 to 70000 for a capacity of 100000."""
    return _read("items_wide.txt")


def get_huge_items():
    """200000 items with weights 1 to 60, generated in memory."""
    return generate_items(200000, 1, 60, seed=20260903, prefix="h")
