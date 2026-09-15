"""You'll implement this."""

from inventory import Inventory


class Solver:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def pack(self, capacity):
        """Pack every item into boxes that each hold at most `capacity` weight.

        Return a list of boxes, each box a list of item names. Every item appears in
        exactly one box. Use as few boxes as you reasonably can: the tests accept any
        packing that uses no more boxes than first-fit decreasing would.
        Raise ValueError when an item is heavier than `capacity`.
        """
        pass
