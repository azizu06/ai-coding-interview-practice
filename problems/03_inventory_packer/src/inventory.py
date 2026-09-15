"""Read this first."""

from collections import namedtuple

Item = namedtuple("Item", ["name", "weight"])


class Inventory:
    def __init__(self, pairs=()):
        self._items = []
        self._names = set()
        for name, weight in pairs:
            self.add_item(name, weight)

    def add_item(self, name, weight):
        if not isinstance(weight, int) or weight < 0:
            return False
        if name in self._names:
            return False
        self._names.add(name)
        self._items.append(Item(name, weight))
        return True

    def total_weight(self):
        return sum(item.weight for item in self._items)

    def items(self):
        return list(self._items)

    def items_by_weight(self):
        return sorted(self._items, key=lambda item: (item.weight, item.name), reverse=True)

    def heaviest(self):
        ordered = self.items_by_weight()
        return ordered[0] if ordered else None

    def __len__(self):
        return len(self._items)

    def __contains__(self, name):
        return name in self._names
