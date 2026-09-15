"""Read this first."""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class WordList:
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
        if len(word) >= self.max_length:
            return False
        for letter in word:
            if letter not in ALPHABET:
                return False
        return True

    def contains_as_substring(self, needle, haystack):
        if needle == haystack:
            return False
        return needle in haystack

    def words(self):
        return list(self._words)

    def longest_length(self):
        return max((len(word) for word in self._words), default=0)

    def __len__(self):
        return len(self._words)

    def __iter__(self):
        return iter(self._words)

    def __contains__(self, word):
        return word in self._words
