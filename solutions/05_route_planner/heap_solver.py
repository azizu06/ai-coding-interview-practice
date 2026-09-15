"""Middle rung of the ladder: heap Dijkstra, but every query explores the whole map.

This is the answer most people reach for right after the O(V^2) version. The priority
queue removes the linear scan for the closest unsettled stop, so a single query drops from
O(V^2) to O(E log V). It clears the 10000 stop map easily. It still loses on the 90000
stop map, because each of the 100 trips settles all 90000 stops even though the two ends
are fifteen blocks apart, and because `neighbors()` sorts a fresh list every time it is
called. See solver.py for the version that stops early and caches the adjacency table.
"""

import heapq

from road_map import RoadMap


class Solver:
    def __init__(self, road_map: RoadMap):
        self.road_map = road_map

    def _distances(self, start):
        best = {start: 0}
        settled = {}
        heap = [(0, start)]
        while heap:
            minutes, stop = heapq.heappop(heap)
            if stop in settled:
                continue
            settled[stop] = minutes
            for neighbor, road_minutes in self.road_map.neighbors(stop):
                candidate = minutes + road_minutes
                if neighbor not in settled and candidate < best.get(neighbor, candidate + 1):
                    best[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))
        return settled

    def shortest_time(self, start, end):
        if start not in self.road_map or end not in self.road_map:
            return None
        return self._distances(start).get(end)

    def nearest_stops(self, start, k):
        if start not in self.road_map or k <= 0:
            return []
        found = [(minutes, stop) for stop, minutes in self._distances(start).items() if stop != start]
        found.sort()
        return [(stop, minutes) for minutes, stop in found[:k]]
