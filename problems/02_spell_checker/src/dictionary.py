"""Read this first."""

PUNCTUATION = ".,;:!?\"'()[]"


class Dictionary:
    def __init__(self, raw_words=()):
        self._words = set()
        for raw in raw_words:
            self.add_word(raw)

    @staticmethod
    def normalize(word):
        return word.strip(PUNCTUATION).strip().lower()

    def add_word(self, word):
        normalized = self.normalize(word)
        if normalized in self._words:
            return False
        self._words.add(normalized)
        return True

    def is_word(self, word):
        return self.normalize(word) in self._words

    def words(self):
        return sorted(self._words)

    def words_of_length(self, length):
        return sorted(word for word in self._words if len(word) == length)

    def max_word_length(self):
        return max((len(word) for word in self._words), default=0)

    def __len__(self):
        return len(self._words)

    def __contains__(self, word):
        return self.is_word(word)
