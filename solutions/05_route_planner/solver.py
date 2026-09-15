"""Reference solution: heap Dijkstra with early exit over a cached adjacency table.

The adjacency table is read out of the RoadMap once, so repeated queries do not pay for
sorted neighbor lists every time. `shortest_time` stops as soon as the destination is
popped from the heap, and `nearest_stops` stops after k stops have been settled. On a
90000 stop grid a nearby query touches a few thousand stops instead of all of them.
"""

import heapq

from road_map import RoadMap


class Solver:
    def __init__(self, road_map: RoadMap):
        self.road_map = road_map
        self._adjacency = None

    def _links(self):
        if self._adjacency is None:
            self._adjacency = {stop: self.road_map.neighbors(stop) for stop in self.road_map.stops()}
        return self._adjacency

    def _settle(self, start, stop_when):
        """Run Dijkstra from `start`, settling stops until `stop_when(stop, minutes, settled)` says stop."""
        links = self._links()
        best = {start: 0}
        settled = {}
        heap = [(0, start)]
        while heap:
            minutes, stop = heapq.heappop(heap)
            if stop in settled:
                continue
            settled[stop] = minutes
            if stop_when(stop, minutes, settled):
                break
            for neighbor, road_minutes in links[stop]:
                candidate = minutes + road_minutes
                if neighbor not in settled and candidate < best.get(neighbor, candidate + 1):
                    best[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))
        return settled

    def shortest_time(self, start, end):
        if start not in self._links() or end not in self._links():
            return None
        settled = self._settle(start, lambda stop, minutes, done: stop == end)
        return settled.get(end)

    def nearest_stops(self, start, k):
        if start not in self._links() or k <= 0:
            return []
        settled = self._settle(start, lambda stop, minutes, done: len(done) > k)
        found = [(minutes, stop) for stop, minutes in settled.items() if stop != start]
        found.sort()
        return [(stop, minutes) for minutes, stop in found[:k]]
