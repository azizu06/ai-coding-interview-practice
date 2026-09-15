"""Generate the item files for the Inventory Packer problem.

Run from this directory: python gen_data.py
The huge set is not written to disk; see src/items.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from items import generate_items  # noqa: E402


def write(name, items):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        for item_name, weight in items:
            handle.write(f"{item_name} {weight}\n")
    print(f"{name}: {len(items)} items, {os.path.getsize(path)} bytes")


def main():
    write("items_small.txt", generate_items(12, 1, 9, seed=1, prefix="s"))
    write("items_medium.txt", generate_items(2000, 1, 60, seed=2, prefix="m"))
    write("items_large.txt", generate_items(40000, 1, 60, seed=3, prefix="l"))
    write("items_wide.txt", generate_items(20000, 1, 70000, seed=4, prefix="w"))


if __name__ == "__main__":
    main()
