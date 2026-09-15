import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph_data import (  # noqa: E402
    get_dense_graph,
    get_dense_queries,
    get_example_graph,
    get_large_graph,
    get_large_queries,
    get_medium_graph,
    get_medium_queries,
    get_small_graph,
    get_small_queries,
)
from social_graph import SocialGraph  # noqa: E402
from solver import Solver  # noqa: E402


def recommend(pairs, user, limit=5):
    return Solver(SocialGraph(pairs)).recommend(user, limit)


def shared_total(graph, queries, limit=10):
    """Sum of the shared friend counts over every recommendation made."""
    solver = Solver(graph)
    total = 0
    for user in queries:
        for _candidate, shared in solver.recommend(user, limit):
            total += shared
    return total


class TestSolverCorrectness(unittest.TestCase):
    def test_unknown_user_gets_nothing(self):
        self.assertEqual(Solver(get_example_graph()).recommend(404, 5), [])

    def test_limit_of_zero_gets_nothing(self):
        self.assertEqual(Solver(get_example_graph()).recommend(1, 0), [])

    def test_triangle_has_nothing_left_to_suggest(self):
        self.assertEqual(recommend([(1, 2), (2, 3), (3, 1)], 1), [])

    def test_one_shared_friend(self):
        self.assertEqual(recommend([(1, 2), (2, 3)], 1), [(3, 1)])

    def test_more_shared_friends_ranks_higher(self):
        pairs = [(1, 2), (1, 3), (2, 9), (3, 9), (2, 8)]
        self.assertEqual(recommend(pairs, 1), [(9, 2), (8, 1)])

    def test_existing_friends_are_never_suggested(self):
        pairs = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        self.assertEqual(recommend(pairs, 1), [(4, 2)])

    # def test_example_graph_user_1(self):
    #     expected = "????"
    #     self.assertEqual(Solver(get_example_graph()).recommend(1, 5), expected)

    # def test_example_graph_user_7(self):
    #     expected = "????"
    #     self.assertEqual(Solver(get_example_graph()).recommend(7, 5), expected)

    # def test_limit_truncates_the_ranking(self):
    #     expected = "????"
    #     self.assertEqual(Solver(get_example_graph()).recommend(7, 1), expected)

    # def test_a_tie_goes_to_the_smaller_id(self):
    #     pairs = [(1, 2), (1, 3), (2, 5), (3, 5), (2, 4), (3, 4)]
    #     expected = "????"
    #     self.assertEqual(recommend(pairs, 1), expected)

    # def test_friend_of_a_friend_of_a_friend_is_too_far(self):
    #     expected = "????"
    #     self.assertEqual(recommend([(1, 2), (2, 3), (3, 4)], 1), expected)


# Timed tests. Uncomment them for task 6.
# Each one recommends 10 people for every user in its query list and checks both
# the total number of shared friends reported and the time taken.

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.small = (get_small_graph(), get_small_queries())
        cls.medium = (get_medium_graph(), get_medium_queries())
        cls.large = (get_large_graph(), get_large_queries())
        cls.dense = (get_dense_graph(), get_dense_queries())

    # def test_small_200_users(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = shared_total(*self.small)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 300)
    #     self.assertLess(elapsed, expected_time, f"200 users: {elapsed:.2f}s, need < {expected_time}s")

    # def test_medium_2000_users(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = shared_total(*self.medium)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 763)
    #     self.assertLess(elapsed, expected_time, f"2000 users: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_50000_users(self):
    #     expected_time = 1.0
    #     start = time.perf_counter()
    #     total = shared_total(*self.large)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 6028)
    #     self.assertLess(elapsed, expected_time, f"50000 users, 500 queries: {elapsed:.2f}s, need < {expected_time}s")

    # def test_dense_150_friends_each(self):
    #     expected_time = 1.5
    #     start = time.perf_counter()
    #     total = shared_total(*self.dense)
    #     elapsed = time.perf_counter() - start
    #     self.assertEqual(total, 145887)
    #     self.assertLess(elapsed, expected_time, f"8000 users, 150 friends each: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
