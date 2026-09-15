"""Read this first."""


class RoadMap:
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
        self._roads[a][b] = minutes

    def stops(self):
        return sorted(self._roads)

    def neighbors(self, stop):
        return sorted(self._roads[stop].items())

    def travel_time(self, a, b):
        return self._roads[a].get(b)

    def road_count(self):
        return sum(len(links) for links in self._roads.values()) // 2

    def __len__(self):
        return len(self._roads)

    def __contains__(self, name):
        return name in self._roads
