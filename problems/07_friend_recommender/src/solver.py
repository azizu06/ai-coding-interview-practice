"""You'll implement this."""

from social_graph import SocialGraph


class Solver:
    def __init__(self, graph: SocialGraph):
        self.graph = graph

    def recommend(self, user, limit):
        """Suggest up to `limit` new friends for `user`.

        A candidate is anyone who shares at least one friend with `user` but
        is neither `user` nor already a friend of `user`. Candidates are
        ranked by how many friends they share with `user`, highest first,
        and ties are broken by the smaller user id.

        Return a list of (candidate, shared_friend_count) pairs.
        A user with no friends gets an empty list.
        """
        pass
