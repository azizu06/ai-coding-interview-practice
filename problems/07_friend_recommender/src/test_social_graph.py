import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from social_graph import SocialGraph  # noqa: E402


class TestSocialGraph(unittest.TestCase):
    def test_friendship_is_mutual(self):
        graph = SocialGraph([(1, 2)])
        self.assertEqual(graph.friends_of(1), [2])
        self.assertEqual(graph.friends_of(2), [1])

    def test_friends_keep_insertion_order(self):
        graph = SocialGraph([(1, 9), (1, 4), (1, 7)])
        self.assertEqual(graph.friends_of(1), [9, 4, 7])

    def test_self_friendship_is_ignored(self):
        graph = SocialGraph([(1, 1), (1, 2)])
        self.assertEqual(graph.friends_of(1), [2])

    def test_are_friends(self):
        graph = SocialGraph([(1, 2), (2, 3)])
        self.assertTrue(graph.are_friends(1, 2))
        self.assertTrue(graph.are_friends(2, 1))
        self.assertFalse(graph.are_friends(1, 3))

    def test_nobody_is_their_own_friend(self):
        graph = SocialGraph([(1, 2)])
        self.assertFalse(graph.are_friends(1, 1))

    def test_users_are_sorted(self):
        graph = SocialGraph([(9, 2), (4, 9)])
        self.assertEqual(graph.users(), [2, 4, 9])

    def test_membership_and_length(self):
        graph = SocialGraph([(1, 2), (2, 3)])
        self.assertIn(2, graph)
        self.assertNotIn(7, graph)
        self.assertEqual(len(graph), 3)

    def test_friendship_count(self):
        graph = SocialGraph([(1, 2), (2, 3), (3, 1)])
        self.assertEqual(graph.friendship_count(), 3)

    def test_degree(self):
        graph = SocialGraph([(1, 2), (1, 3), (1, 4)])
        self.assertEqual(graph.degree(1), 3)
        self.assertEqual(graph.degree(2), 1)

    # def test_duplicate_friendship_is_ignored(self):
    #     graph = SocialGraph([(1, 2), (2, 1), (1, 2)])
    #     expected = "????"
    #     self.assertEqual(graph.friends_of(1), expected)

    # def test_repeats_do_not_inflate_degree(self):
    #     graph = SocialGraph([(1, 2), (1, 3), (3, 1), (2, 1)])
    #     expected_count = "????"
    #     self.assertEqual(graph.degree(1), expected_count)

    # def test_unknown_user_has_no_friends(self):
    #     graph = SocialGraph([(1, 2)])
    #     expected = "????"
    #     self.assertEqual(graph.friends_of(404), expected)

    # def test_degree_of_unknown_user_is_zero(self):
    #     graph = SocialGraph([(1, 2)])
    #     expected_count = "????"
    #     self.assertEqual(graph.degree(404), expected_count)


if __name__ == "__main__":
    unittest.main()
