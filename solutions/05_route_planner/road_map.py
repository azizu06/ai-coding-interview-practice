"""Read this first."""


class RoadMap:
    """Stops connected by two-way roads, each with a travel time in whole minutes.

    Rules:
      * stops are added by name; adding a name twice is harmless
      * `add_road(a, b, minutes)` connects a and b in both directions
      * both stops must already exist (KeyError otherwise)
      * a road from a stop to itself is rejected (ValueError)
      * minutes must be a positive integer (ValueError otherwise)
      * when a road between the same two stops is added again, the faster time wins
      * `neighbors(stop)` returns (neighbor, minutes) pairs sorted by neighbor name
      * `travel_time(a, b)` returns the minutes of the direct road, or None when there is none
    """

    def __init__(self):
        self._roads = {}

    def add_stop(self, name):
        self._roads.setdefault(name, {})

    def add_road(self, a, b, minutes):
        if a not in self._roads:
            raise KeyError(a)
        if b not in self._roads:
            raise KeyError(b)
        if a == b:
            raise ValueError(f"a road cannot connect {a!r} to itself")
        if not isinstance(minutes, int) or minutes <= 0:
            raise ValueError(f"minutes must be a positive integer, got {minutes!r}")
        current = self._roads[a].get(b)
        if current is None or minutes < current:
            self._roads[a][b] = minutes
            self._roads[b][a] = minutes

    def stops(self):
        return sorted(self._roads)

    def neighbors(self, stop):
        """Direct connections of `stop` as (neighbor, minutes) pairs, sorted by name."""
        return sorted(self._roads[stop].items())

    def travel_time(self, a, b):
        """Minutes for the direct road between a and b, or None when they are not connected."""
        return self._roads[a].get(b)

    def road_count(self):
        """Number of two-way roads."""
        return sum(len(links) for links in self._roads.values()) // 2

    def __len__(self):
        return len(self._roads)

    def __contains__(self, name):
        return name in self._roads
