"""Read this first.

A SocialGraph stores mutual friendships between users. A user is an integer id.

Rules this class follows:
  * a friendship is mutual, so adding (a, b) also makes b a friend of a
  * a user is never their own friend, so add_friendship(a, a) does nothing
  * adding the same friendship a second time changes nothing
  * friends_of() returns friends in the order they were added
  * asking about a user who never appeared is fine: they have no friends

friends_of() hands back the list it stores, so treat the result as read only.
"""


class SocialGraph:
    def __init__(self, pairs=()):
        self._friends = {}
        self._known = set()
        for a, b in pairs:
            self.add_friendship(a, b)

    def add_friendship(self, a, b):
        """Record that a and b are friends. Self pairs and repeats do nothing."""
        if a == b:
            return
        edge = (a, b) if a < b else (b, a)
        if edge in self._known:
            return
        self._known.add(edge)
        self._friends.setdefault(a, []).append(b)
        self._friends.setdefault(b, []).append(a)

    def friends_of(self, user):
        """The friends of `user`, in the order they were added."""
        return self._friends.get(user, [])

    def are_friends(self, a, b):
        """True when a and b are friends of each other."""
        if a == b:
            return False
        return ((a, b) if a < b else (b, a)) in self._known

    def degree(self, user):
        """How many friends `user` has."""
        return len(self.friends_of(user))

    def users(self):
        """Every user id that appears in at least one friendship, sorted."""
        return sorted(self._friends)

    def friendship_count(self):
        """How many distinct friendships the graph holds."""
        return len(self._known)

    def __len__(self):
        return len(self._friends)

    def __contains__(self, user):
        return user in self._friends
