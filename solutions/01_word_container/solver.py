"""Reference solution: a trie of all words, walked from every start position. O(N * M^2) worst case."""

from word_list import WordList

END = "$"


class Solver:
    def __init__(self, word_list: WordList):
        self.word_list = word_list

    def _build_trie(self, words):
        root = {}
        for word in words:
            node = root
            for letter in word:
                node = node.setdefault(letter, {})
            node[END] = True
        return root

    def find_container_words(self):
        words = self.word_list.words()
        root = self._build_trie(words)
        found = []
        for word in words:
            length = len(word)
            hit = False
            for start in range(length):
                node = root
                position = start
                while position < length:
                    node = node.get(word[position])
                    if node is None:
                        break
                    position += 1
                    if END in node and not (start == 0 and position == length):
                        hit = True
                        break
                if hit:
                    break
            if hit:
                found.append(word)
        return sorted(found)
