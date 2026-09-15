"""You'll implement this."""

from dictionary import Dictionary


class Solver:
    def __init__(self, dictionary: Dictionary):
        self.dictionary = dictionary

    def suggest(self, word, max_distance=1):
        """Return every dictionary word within `max_distance` edits of `word`.

        An edit is inserting one letter, deleting one letter, or replacing one letter
        (Levenshtein distance). The query is normalized with `Dictionary.normalize` first.
        The result is sorted alphabetically. A word that is already in the dictionary is
        at distance 0 and is part of its own suggestions. `max_distance` is 1 or 2.
        """
        pass
