"""Read this first."""

PUNCTUATION = ".,;:!?\"'()[]"


class Dictionary:
    """A set of known words.

    Every word that goes in or gets looked up passes through `normalize` first:
      * surrounding whitespace is removed
      * then punctuation around the word is removed (so "Hello!" and "'hello'" both become "hello")
      * then the word is lowercased

    A word that is blank after normalizing is never stored and is never a known word.
    """

    def __init__(self, raw_words=()):
        self._words = set()
        for raw in raw_words:
            self.add_word(raw)

    @staticmethod
    def normalize(word):
        """Return the canonical form of `word` as described in the class docstring."""
        return word.strip().strip(PUNCTUATION).lower()

    def add_word(self, word):
        """Store the normalized form of `word`. Return True when the dictionary grew."""
        normalized = self.normalize(word)
        if not normalized:
            return False
        if normalized in self._words:
            return False
        self._words.add(normalized)
        return True

    def is_word(self, word):
        """True when the normalized form of `word` is in the dictionary."""
        return self.normalize(word) in self._words

    def words(self):
        """All known words, sorted."""
        return sorted(self._words)

    def words_of_length(self, length):
        """All known words with exactly `length` letters, sorted."""
        return sorted(word for word in self._words if len(word) == length)

    def max_word_length(self):
        return max((len(word) for word in self._words), default=0)

    def __len__(self):
        return len(self._words)

    def __contains__(self, word):
        return self.is_word(word)
