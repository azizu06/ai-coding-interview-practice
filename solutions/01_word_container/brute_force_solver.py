"""Brute force reference: compare every pair of words. O(N^2 * M)."""

from word_list import WordList


class Solver:
    def __init__(self, word_list: WordList):
        self.word_list = word_list

    def find_container_words(self):
        words = self.word_list.words()
        found = set()
        for haystack in words:
            for needle in words:
                if self.word_list.contains_as_substring(needle, haystack):
                    found.add(haystack)
                    break
        return sorted(found)
