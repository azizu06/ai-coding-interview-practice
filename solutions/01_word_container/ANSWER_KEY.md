# 01 Word Container: answer key

## The two bugs in `WordList`

1. `is_valid_word` rejects a word whose length equals `max_length`. The check reads
   `len(word) >= self.max_length`, but a maximum length includes that length itself, so it
   must be `len(word) > self.max_length`. The commented-out
   `test_word_exactly_max_length_is_valid` and `test_max_length_word_is_kept` are the two
   that ask for it, and the live `test_word_longer_than_max_is_rejected` is the pair that
   makes the boundary obvious once both are running.
2. `is_valid_word` accepts the empty string. The letter loop never runs for `""`, so the
   function falls through to `return True`. Add an explicit `len(word) == 0` rejection.
   `test_empty_string_is_rejected` and `test_blank_entries_are_dropped` expose it, and
   `main.py` shows an empty word sneaking into the cleaned list.

## Expected values for the `????` tests

See `expected.json`. Highlights: the example words give
`["concatenate", "hotdog", "plate", "sunny"]`; `words_small.txt` has 7 containers; medium 73,
large 1567, huge 4305, long 6.

## Brute force

For every word, check every other word with `contains_as_substring`. With N words of
average length M that is O(N^2 * M). It passes the 500 word test in a few milliseconds and
takes about 2.2 s on 10000 words (budget 0.5 s) and well over 10 s on 25000 words
(budget 1 s). See `brute_force_solver.py`.

## Optimization ladder

| Rung | Idea | Complexity | Passes | Breaks on |
| --- | --- | --- | --- | --- |
| 1 | Nested loop over all pairs | O(N^2 * M) | medium | large, huge |
| 2 | Put all words in a set, then for each word test every substring against the set | O(N * M^3) (M^2 substrings, each hashed in O(M)) | medium, large, huge | long words: 30 words of up to 2000 letters take about 5 s against a 1 s budget |
| 3 | Build a trie of all words, then for each word walk the trie from every start position and stop as soon as a stored word ends | O(N * M^2) worst case, close to O(N * M) on real data because walks die after a few letters | everything | |

The trie is the reference in `solver.py`. The key detail is the "is this the word itself"
check: a terminal node reached from start position 0 that ends at the last letter is the
word itself and must be ignored.

## Good AI prompts

1. "Read word_list.py and write out every rule it actually enforces on a word, then hold
   that list against the README and the commented-out tests in test_word_list.py and tell
   me which rule is off." (Points the agent at the stated behavior rather than asking it to
   hunt for bugs.)
2. "My substring-set solver passes 25000 short words in 0.04 s but takes 5 s on 30 words of
   2000 letters. Explain why the cost grows with the cube of the word length and propose a
   structure whose cost does not." (Gives the agent the measured evidence.)
3. "Write a trie-based find_container_words that treats a word matching itself as a non
   match, and keep the output sorted and de-duplicated." (States the edge case up front.)
4. "Add a test that feeds the same word into the list twice and asserts it still does not
   come back as its own container." (Tightens the weakest spot in the shipped tests.)

## Bad AI prompts

1. "Fix the bugs." (No context about what the class is supposed to do; the agent will guess
   and may change working behavior.)
2. "Make the tests pass." (Invites the agent to edit the tests or hardcode expected counts.)
3. "Make it faster." (No target, no measurement; you will get micro-optimizations of the
   nested loop instead of a different algorithm.)
