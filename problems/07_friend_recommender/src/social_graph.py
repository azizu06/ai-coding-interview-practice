"""Read this first."""


class SocialGraph:
    def __init__(self, pairs=()):
        self._friends = {}
        self._known = set()
        for a, b in pairs:
            self.add_friendship(a, b)

    def add_friendship(self, a, b):
        if a == b:
            return
        edge = (a, b) if a < b else (b, a)
        self._known.add(edge)
        self._friends.setdefault(a, []).append(b)
        self._friends.setdefault(b, []).append(a)

    def friends_of(self, user):
        return self._friends[user]

    def are_friends(self, a, b):
        if a == b:
            return False
        return ((a, b) if a < b else (b, a)) in self._known

    def degree(self, user):
        return len(self.friends_of(user))

    def users(self):
        return sorted(self._friends)

    def friendship_count(self):
        return len(self._known)

    def __len__(self):
        return len(self._friends)

    def __contains__(self, user):
        return user in self._friends
