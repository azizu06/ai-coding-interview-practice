"""Reference solution.

Count friends of friends with Counter.update, which does the counting in C for
a whole friend list at a time, then pull the top `limit` with a heap instead of
sorting every candidate.

The part that matters most is hoisting the user's own friends into a set once
per query. Testing `candidate in graph.friends_of(user)` inside the candidate
loop scans a list, which turns an O(candidates) filter into O(candidates * d)
and falls over on the dense graph.
"""

import heapq
from collections import Counter

from social_graph import SocialGraph


class Solver:
    def __init__(self, graph: SocialGraph):
        self.graph = graph

    def recommend(self, user, limit):
        graph = self.graph
        friends = graph.friends_of(user)
        if not friends or limit <= 0:
            return []
        counts = Counter()
        for friend in friends:
            counts.update(graph.friends_of(friend))
        counts.pop(user, None)
        for friend in friends:
            counts.pop(friend, None)
        ordered = heapq.nsmallest(limit, ((-n, c) for c, n in counts.items()))
        return [(c, -n) for n, c in ordered]
