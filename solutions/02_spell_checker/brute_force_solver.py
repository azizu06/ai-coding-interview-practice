"""Brute force reference: edit distance against every dictionary word of a plausible length. O(N * M^2) per query."""

from dictionary import Dictionary


def edit_distance(a, b):
    previous = list(range(len(b) + 1))
    for i, letter_a in enumerate(a, 1):
        current = [i]
        for j, letter_b in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (letter_a != letter_b)))
        previous = current
    return previous[-1]


class Solver:
    def __init__(self, dictionary: Dictionary):
        self.dictionary = dictionary

    def suggest(self, word, max_distance=1):
        query = self.dictionary.normalize(word)
        if not query:
            return []
        found = []
        for length in range(len(query) - max_distance, len(query) + max_distance + 1):
            for candidate in self.dictionary.words_of_length(length):
                if edit_distance(query, candidate) <= max_distance:
                    found.append(candidate)
        return sorted(found)
