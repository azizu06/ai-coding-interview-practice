"""Runnable demo. Try: python src/main.py"""

from map_data import get_example_map
from road_map import RoadMap
from solver import Solver


def build_map(stops, roads):
    road_map = RoadMap()
    for stop in stops:
        road_map.add_stop(stop)
    for a, b, minutes in roads:
        road_map.add_road(a, b, minutes)
    return road_map


def main():
    print("BEGIN route planner demo")
    stops, roads = get_example_map()
    road_map = build_map(stops, roads)
    road_map.add_road("airport", "downtown", 30)
    print(f"{len(road_map)} stops, {road_map.road_count()} roads")
    for stop in road_map.stops():
        print(f"  {stop:9} -> {road_map.neighbors(stop)}")
    print(f"direct airport to downtown: {road_map.travel_time('airport', 'downtown')}")
    print(f"direct downtown to airport: {road_map.travel_time('downtown', 'airport')}")
    solver = Solver(road_map)
    for start, end in [("airport", "beach"), ("island", "beach"), ("harbor", "harbor")]:
        print(f"shortest {start} -> {end}: {solver.shortest_time(start, end)}")
    print(f"nearest 3 to downtown: {solver.nearest_stops('downtown', 3)}")
    print("END route planner demo")


if __name__ == "__main__":
    main()
