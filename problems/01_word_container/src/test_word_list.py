import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from word_list import WordList  # noqa: E402


class TestWordListValidation(unittest.TestCase):
    def test_plain_lowercase_word_is_valid(self):
        word_list = WordList([])
        self.assertTrue(word_list.is_valid_word("hello"))

    def test_uppercase_is_rejected(self):
        word_list = WordList([])
        self.assertFalse(word_list.is_valid_word("Hello"))

    def test_digits_and_punctuation_are_rejected(self):
        word_list = WordList([])
        self.assertFalse(word_list.is_valid_word("h3llo"))
        self.assertFalse(word_list.is_valid_word("sun-ny"))
        self.assertFalse(word_list.is_valid_word("two words"))

    def test_word_longer_than_max_is_rejected(self):
        word_list = WordList([], max_length=5)
        self.assertFalse(word_list.is_valid_word("abcdef"))

    # def test_word_exactly_max_length_is_valid(self):
    #     word_list = WordList([], max_length=5)
    #     expected = "????"
    #     self.assertEqual(word_list.is_valid_word("abcde"), expected)

    # def test_empty_string_is_rejected(self):
    #     word_list = WordList([])
    #     expected = "????"
    #     self.assertEqual(word_list.is_valid_word(""), expected)


class TestWordListBuilding(unittest.TestCase):
    def test_keeps_order_of_first_appearance(self):
        word_list = WordList(["pear", "apple", "fig"])
        self.assertEqual(word_list.words(), ["pear", "apple", "fig"])

    def test_duplicates_are_dropped(self):
        word_list = WordList(["fig", "fig", "pear", "fig"])
        self.assertEqual(word_list.words(), ["fig", "pear"])
        self.assertEqual(len(word_list), 2)

    def test_surrounding_whitespace_is_stripped(self):
        word_list = WordList(["  fig\n", "pear "])
        self.assertEqual(word_list.words(), ["fig", "pear"])

    def test_invalid_entries_are_dropped(self):
        word_list = WordList(["fig", "Pear", "a1", "plum"])
        self.assertEqual(word_list.words(), ["fig", "plum"])

    # def test_blank_entries_are_dropped(self):
    #     word_list = WordList(["fig", "", "   ", "plum"])
    #     expected_count = "????"
    #     self.assertEqual(len(word_list), expected_count)

    # def test_max_length_word_is_kept(self):
    #     word_list = WordList(["abc", "abcd", "abcde"], max_length=4)
    #     expected = "????"
    #     self.assertEqual(word_list.words(), expected)

    def test_longest_length(self):
        self.assertEqual(WordList(["a", "abc", "ab"]).longest_length(), 3)
        self.assertEqual(WordList([]).longest_length(), 0)


class TestContainsAsSubstring(unittest.TestCase):
    def setUp(self):
        self.word_list = WordList([])

    def test_substring_in_middle(self):
        self.assertTrue(self.word_list.contains_as_substring("cat", "concatenate"))

    def test_substring_at_end(self):
        self.assertTrue(self.word_list.contains_as_substring("dog", "hotdog"))

    def test_same_word_does_not_count(self):
        self.assertFalse(self.word_list.contains_as_substring("dog", "dog"))

    def test_unrelated_words(self):
        self.assertFalse(self.word_list.contains_as_substring("cat", "hotdog"))

    def test_longer_needle_never_matches(self):
        self.assertFalse(self.word_list.contains_as_substring("hotdog", "dog"))


if __name__ == "__main__":
    unittest.main()
