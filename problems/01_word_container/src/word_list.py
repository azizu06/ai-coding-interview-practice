"""Read this first."""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class WordList:
    """A cleaned, de-duplicated list of words.

    A word is valid when it:
      * contains only the lowercase letters a to z
      * has at least one character
      * has at most `max_length` characters (max_length itself is allowed)

    Invalid words and repeated words are dropped when the list is built.
    Order of first appearance is kept.
    """

    DEFAULT_MAX_LENGTH = 2000

    def __init__(self, raw_words, max_length=DEFAULT_MAX_LENGTH):
        self.max_length = max_length
        self._words = []
        seen = set()
        for raw in raw_words:
            word = raw.strip()
            if not self.is_valid_word(word):
                continue
            if word in seen:
                continue
            seen.add(word)
            self._words.append(word)

    def is_valid_word(self, word):
        """Return True when `word` follows the rules in the class docstring."""
        if len(word) >= self.max_length:
            return False
        for letter in word:
            if letter not in ALPHABET:
                return False
        return True

    def contains_as_substring(self, needle, haystack):
        """Return True when `needle` appears inside `haystack` and they are not the same word."""
        if needle == haystack:
            return False
        return needle in haystack

    def words(self):
        """A copy of the words in list order."""
        return list(self._words)

    def longest_length(self):
        """Length of the longest word, or 0 for an empty list."""
        return max((len(word) for word in self._words), default=0)

    def __len__(self):
        return len(self._words)

    def __iter__(self):
        return iter(self._words)

    def __contains__(self, word):
        return word in self._words
