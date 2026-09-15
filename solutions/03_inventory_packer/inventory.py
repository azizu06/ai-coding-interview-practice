"""Read this first."""

from collections import namedtuple

Item = namedtuple("Item", ["name", "weight"])


class Inventory:
    """Items waiting to be packed.

    Rules:
      * every item has a unique name
      * every weight is a positive integer (zero and negatives are rejected)
      * `add_item` returns True when the item was stored and False when it was rejected
      * `items_by_weight` lists the heaviest items first; equal weights are ordered by name
    """

    def __init__(self, pairs=()):
        self._items = []
        self._names = set()
        for name, weight in pairs:
            self.add_item(name, weight)

    def add_item(self, name, weight):
        """Store an item. Return True when it was stored."""
        if not isinstance(weight, int) or weight <= 0:
            return False
        if name in self._names:
            return False
        self._names.add(name)
        self._items.append(Item(name, weight))
        return True

    def total_weight(self):
        return sum(item.weight for item in self._items)

    def items(self):
        """Items in the order they were added."""
        return list(self._items)

    def items_by_weight(self):
        """Heaviest first. Items of equal weight are ordered by name."""
        return sorted(self._items, key=lambda item: (-item.weight, item.name))

    def heaviest(self):
        """The heaviest item, or None when empty."""
        ordered = self.items_by_weight()
        return ordered[0] if ordered else None

    def __len__(self):
        return len(self._items)

    def __contains__(self, name):
        return name in self._names
