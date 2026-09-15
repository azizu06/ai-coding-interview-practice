"""You'll implement this."""

from road_map import RoadMap


class Solver:
    def __init__(self, road_map: RoadMap):
        self.road_map = road_map

    def shortest_time(self, start, end):
        """Fewest minutes to travel from `start` to `end`, or None when no route exists.

        Travelling from a stop to itself takes 0 minutes.
        """
        pass

    def nearest_stops(self, start, k):
        """The `k` stops closest to `start` by travel time, not counting `start` itself.

        Return a list of (stop, minutes) pairs sorted by minutes, then by name. Return
        fewer than `k` pairs when fewer stops are reachable.
        """
        pass
