"""Middle rung: friends of friends counted in a plain Python loop, with the
"is this already a friend" test done against the friend list itself.

Correct, and fine while degrees are small. On the dense graph every query walks
thousands of candidates and scans a 150 entry list for each one, so the filter
alone costs O(candidates * degree).
"""

from social_graph import SocialGraph


class Solver:
    def __init__(self, graph: SocialGraph):
        self.graph = graph

    def recommend(self, user, limit):
        graph = self.graph
        counts = {}
        for friend in graph.friends_of(user):
            for candidate in graph.friends_of(friend):
                counts[candidate] = counts.get(candidate, 0) + 1
        result = []
        for candidate, shared in counts.items():
            if candidate == user:
                continue
            if candidate in graph.friends_of(user):
                continue
            result.append((candidate, shared))
        result.sort(key=lambda pair: (-pair[1], pair[0]))
        return result[:limit]
