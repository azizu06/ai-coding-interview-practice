"""Runnable demo. Try: python src/main.py"""

from dictionary import Dictionary
from solver import Solver
from word_files import get_example_words


def main():
    print("BEGIN spell checker demo")
    dictionary = Dictionary(get_example_words() + ["Apple!", "", "  "])
    print(f"dictionary ({len(dictionary)} words): {dictionary.words()}")
    print("normalize:")
    for raw in ["Apple", "grape.", " 'bread' ", "GREAT!  "]:
        print(f"  {raw!r} -> {Dictionary.normalize(raw)!r}")
    print("is_word:")
    for raw in ["apple", "Apple", "appel", "graph?", ""]:
        print(f"  {raw!r}: {dictionary.is_word(raw)}")
    solver = Solver(dictionary)
    print("suggestions:")
    for raw in ["appel", "grap", "tread", "bred"]:
        print(f"  {raw!r}: {solver.suggest(raw)}")
    print(f"  'grate' within 2 edits: {solver.suggest('grate', max_distance=2)}")
    print("END spell checker demo")


if __name__ == "__main__":
    main()
