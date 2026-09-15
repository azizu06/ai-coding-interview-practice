"""Runnable demo. Try: python src/main.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph_data import get_example_graph  # noqa: E402
from solver import Solver  # noqa: E402


def main():
    print("=== BEGIN friend recommender demo ===")
    graph = get_example_graph()
    print(f"users: {graph.users()}")
    print(f"friendships: {graph.friendship_count()}")
    for user in graph.users():
        print(f"  {user}: friends {graph.friends_of(user)} (degree {graph.degree(user)})")
    print()
    print(f"are 1 and 2 friends? {graph.are_friends(1, 2)}")
    print(f"are 1 and 5 friends? {graph.are_friends(1, 5)}")
    try:
        print(f"friends of user 404, who is in no friendship: {graph.friends_of(404)}")
    except Exception as exc:  # noqa: BLE001
        print(f"friends of user 404, who is in no friendship: raised {type(exc).__name__}")
    print()
    solver = Solver(graph)
    for user in (1, 4, 7, 8):
        print(f"recommend for {user}: {solver.recommend(user, 3)}")
    print("=== END friend recommender demo ===")


if __name__ == "__main__":
    main()
