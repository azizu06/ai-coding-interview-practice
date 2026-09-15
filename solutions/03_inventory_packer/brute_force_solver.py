"""Brute force reference: first-fit decreasing, scanning every open box for each item. O(N * B)."""

from inventory import Inventory


class Solver:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def pack(self, capacity):
        boxes = []
        remaining = []
        for item in self.inventory.items_by_weight():
            if item.weight > capacity:
                raise ValueError(f"{item.name} weighs {item.weight}, more than capacity {capacity}")
            for index, space in enumerate(remaining):
                if space >= item.weight:
                    boxes[index].append(item.name)
                    remaining[index] = space - item.weight
                    break
            else:
                boxes.append([item.name])
                remaining.append(capacity - item.weight)
        return boxes
