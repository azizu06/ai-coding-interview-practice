"""Brute force reference: Dijkstra with a linear scan for the closest unsettled stop. O(V^2) per query."""

from road_map import RoadMap


class Solver:
    def __init__(self, road_map: RoadMap):
        self.road_map = road_map

    def _distances(self, start):
        road_map = self.road_map
        distance = {stop: None for stop in road_map.stops()}
        distance[start] = 0
        unsettled = set(distance)
        while unsettled:
            current = None
            for stop in unsettled:
                if distance[stop] is not None and (current is None or distance[stop] < distance[current]):
                    current = stop
            if current is None:
                break
            unsettled.remove(current)
            for neighbor, minutes in road_map.neighbors(current):
                candidate = distance[current] + minutes
                if distance[neighbor] is None or candidate < distance[neighbor]:
                    distance[neighbor] = candidate
        return distance

    def shortest_time(self, start, end):
        return self._distances(start)[end]

    def nearest_stops(self, start, k):
        distance = self._distances(start)
        reachable = [(minutes, stop) for stop, minutes in distance.items() if minutes is not None and stop != start]
        reachable.sort()
        return [(stop, minutes) for minutes, stop in reachable[:k]]
