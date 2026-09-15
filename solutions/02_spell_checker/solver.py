"""Reference solution: a deletion-neighborhood index (the SymSpell idea).

Every dictionary word is stored under every string you can make by deleting up to
`max_distance` letters from it. A query is looked up under its own deletions. Any word
within `max_distance` edits must share one of those keys, so the candidate set is tiny
and only the candidates get a real edit-distance check.
"""

from dictionary import Dictionary


def edit_distance(a, b):
    previous = list(range(len(b) + 1))
    for i, letter_a in enumerate(a, 1):
        current = [i]
        for j, letter_b in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (letter_a != letter_b)))
        previous = current
    return previous[-1]


def deletions(word, depth):
    """The word itself plus every string reachable by deleting up to `depth` letters."""
    result = {word}
    frontier = {word}
    for _ in range(depth):
        next_frontier = set()
        for item in frontier:
            for i in range(len(item)):
                next_frontier.add(item[:i] + item[i + 1:])
        result |= next_frontier
        frontier = next_frontier
    return result


class Solver:
    def __init__(self, dictionary: Dictionary):
        self.dictionary = dictionary
        self._indexes = {}

    def _index(self, depth):
        index = self._indexes.get(depth)
        if index is None:
            index = {}
            for word in self.dictionary.words():
                for key in deletions(word, depth):
                    index.setdefault(key, []).append(word)
            self._indexes[depth] = index
        return index

    def suggest(self, word, max_distance=1):
        query = self.dictionary.normalize(word)
        if not query:
            return []
        index = self._index(max_distance)
        candidates = set()
        for key in deletions(query, max_distance):
            candidates.update(index.get(key, ()))
        return sorted(w for w in candidates if edit_distance(query, w) <= max_distance)
