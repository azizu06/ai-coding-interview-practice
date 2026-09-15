import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dictionary import Dictionary  # noqa: E402


class TestNormalize(unittest.TestCase):
    def test_lowercases(self):
        self.assertEqual(Dictionary.normalize("Hello"), "hello")

    def test_strips_whitespace(self):
        self.assertEqual(Dictionary.normalize("  hello "), "hello")

    def test_strips_trailing_punctuation(self):
        self.assertEqual(Dictionary.normalize("hello!"), "hello")

    def test_strips_quotes(self):
        self.assertEqual(Dictionary.normalize("'hello'"), "hello")

    def test_keeps_inner_punctuation(self):
        self.assertEqual(Dictionary.normalize("don't"), "don't")

    # def test_punctuation_then_whitespace(self):
    #     expected = "????"
    #     self.assertEqual(Dictionary.normalize("Hello! "), expected)

    # def test_whitespace_around_quotes(self):
    #     expected = "????"
    #     self.assertEqual(Dictionary.normalize(" 'quoted' "), expected)


class TestDictionary(unittest.TestCase):
    def test_words_are_stored_normalized(self):
        dictionary = Dictionary(["Apple", "grape."])
        self.assertEqual(dictionary.words(), ["apple", "grape"])

    def test_is_word_normalizes_lookup(self):
        dictionary = Dictionary(["apple"])
        self.assertTrue(dictionary.is_word("Apple!"))
        self.assertFalse(dictionary.is_word("appel"))

    def test_add_word_reports_growth(self):
        dictionary = Dictionary()
        self.assertTrue(dictionary.add_word("apple"))
        self.assertFalse(dictionary.add_word("APPLE"))
        self.assertEqual(len(dictionary), 1)

    def test_words_of_length(self):
        dictionary = Dictionary(["apple", "fig", "pear", "plum"])
        self.assertEqual(dictionary.words_of_length(4), ["pear", "plum"])
        self.assertEqual(dictionary.words_of_length(9), [])

    def test_max_word_length(self):
        self.assertEqual(Dictionary(["fig", "banana"]).max_word_length(), 6)
        self.assertEqual(Dictionary().max_word_length(), 0)

    # def test_blank_words_are_not_stored(self):
    #     dictionary = Dictionary(["apple", "", "   ", "!"])
    #     expected_count = "????"
    #     self.assertEqual(len(dictionary), expected_count)

    # def test_add_blank_word_returns_false(self):
    #     dictionary = Dictionary()
    #     expected = "????"
    #     self.assertEqual(dictionary.add_word("  "), expected)
    #     self.assertEqual(len(dictionary), 0)

    # def test_empty_string_is_never_a_word(self):
    #     dictionary = Dictionary(["apple", ""])
    #     expected = "????"
    #     self.assertEqual(dictionary.is_word(""), expected)
    #     self.assertEqual(dictionary.is_word("?"), expected)


if __name__ == "__main__":
    unittest.main()
