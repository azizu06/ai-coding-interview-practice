"""Runnable demo. Try: python src/main.py"""

from solver import Solver
from word_list import WordList
from words import get_example_words


def main():
    print("BEGIN word container demo")
    raw = get_example_words() + ["", "Cat", "cat", "sun-ny"]
    word_list = WordList(raw)
    print(f"raw input ({len(raw)} entries): {raw}")
    print(f"valid unique words ({len(word_list)}): {word_list.words()}")
    print(f"longest word length: {word_list.longest_length()}")
    print("pairwise containment checks:")
    for needle in ["cat", "dog", "ate"]:
        for haystack in ["concatenate", "hotdog", "plate"]:
            hit = word_list.contains_as_substring(needle, haystack)
            print(f"  {needle!r} in {haystack!r}: {hit}")
    solver = Solver(word_list)
    result = solver.find_container_words()
    print(f"container words: {result}")
    print("END word container demo")


if __name__ == "__main__":
    main()
