"""Reference solution: best-fit decreasing with boxes bucketed by remaining capacity.

Items go in heaviest first. Open boxes are grouped by how much room they have left, and
the distinct room values are kept in a sorted list so the tightest box that still fits an
item is one bisect away. Each item costs O(log C) plus a small list edit, so 200000 items
pack in well under a second.
"""

from bisect import bisect_left, insort

from inventory import Inventory


class Solver:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def pack(self, capacity):
        boxes = []
        buckets = {}
        room_values = []
        for item in self.inventory.items_by_weight():
            weight = item.weight
            if weight > capacity:
                raise ValueError(f"{item.name} weighs {weight}, more than capacity {capacity}")
            position = bisect_left(room_values, weight)
            if position == len(room_values):
                box_index = len(boxes)
                boxes.append([item.name])
                room = capacity - weight
            else:
                old_room = room_values[position]
                bucket = buckets[old_room]
                box_index = bucket.pop()
                if not bucket:
                    del buckets[old_room]
                    del room_values[position]
                boxes[box_index].append(item.name)
                room = old_room - weight
            if room > 0:
                bucket = buckets.get(room)
                if bucket is None:
                    buckets[room] = [box_index]
                    insort(room_values, room)
                else:
                    bucket.append(box_index)
        return boxes
