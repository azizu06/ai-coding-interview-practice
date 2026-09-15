"""Brute force: look at every user in the graph and intersect friend lists.

Cost per query is O(N log N) for the user list plus O(N * d) for the
intersections. Fine on a couple of thousand users, hopeless on fifty thousand.
"""

from social_graph import SocialGraph


class Solver:
    def __init__(self, graph: SocialGraph):
        self.graph = graph

    def recommend(self, user, limit):
        graph = self.graph
        mine = set(graph.friends_of(user))
        if not mine or limit <= 0:
            return []
        result = []
        for other in graph.users():
            if other == user or other in mine:
                continue
            shared = len(mine.intersection(graph.friends_of(other)))
            if shared:
                result.append((other, shared))
        result.sort(key=lambda pair: (-pair[1], pair[0]))
        return result[:limit]
