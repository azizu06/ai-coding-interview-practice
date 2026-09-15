# 02 Spell Checker: answer key

## The two bugs in `Dictionary`

1. `normalize` strips punctuation before whitespace. The docstring promises whitespace
   first, then punctuation. With the wrong order `"Hello! "` becomes `"hello!"` because the
   trailing space shields the exclamation mark. Fix: `word.strip().strip(PUNCTUATION).lower()`.
   `test_punctuation_then_whitespace` and `test_whitespace_around_quotes` expose it.
2. `add_word` stores a word that is blank after normalizing. `Dictionary(["apple", "", "!"])`
   ends up with two entries and `is_word("")` returns True. Fix: return False when the
   normalized word is empty. `test_blank_words_are_not_stored`,
   `test_add_blank_word_returns_false` and `test_empty_string_is_never_a_word` expose it.
   `main.py` shows the phantom blank word in the printed dictionary.

## Expected values for the `????` tests

See `expected.json`. Totals across all queries: medium 34, large 572, huge 6535, distance
two 973 suggestions.

## Brute force

Normalize the query, then compute Levenshtein distance against every dictionary word whose
length is within `max_distance` of the query length. Each comparison is O(M^2), so a query
costs O(N * M^2). On the 50000 word dictionary that is about 65 ms per query: fine for 20
queries, hopeless for 300 (about 20 s against a 1 s budget). See `brute_force_solver.py`.

## Optimization ladder

| Rung | Idea | Complexity per query | Passes | Breaks on |
| --- | --- | --- | --- | --- |
| 1 | Edit distance against every word of a plausible length | O(N * M^2) | medium | large, huge, distance two |
| 2 | Generate every string one edit away from the query (about 54 * M of them) and test each against the word set | O(26 * M) lookups | medium, large, huge | distance two: two rounds of edits is about 200000 candidates per query, about 6 s for 200 queries |
| 3 | Deletion neighborhood index (SymSpell): store each word under every string made by deleting up to d letters, look the query up under its own deletions, verify the few candidates with real edit distance | O(M^d) lookups per query after an O(N * M^d) index build | everything | |

The index for d = 1 on 50000 words has about 430000 keys and builds in about 0.1 s. The
reference builds indexes lazily per distance so the d = 2 index is only built for the
medium dictionary (about 190000 keys, 0.05 s).

## Good AI prompts

1. "Here is the Dictionary docstring and the normalize implementation. Walk through
   normalize('Hello! ') step by step and tell me where the output stops matching the
   docstring." (Concrete input, concrete contract.)
2. "Generating all two-edit variants of a query is 200000 strings. Is there an index over
   the dictionary that lets me find words within two edits with far fewer lookups? Explain
   the invariant that makes it correct before writing code." (Asks for the idea and the
   proof, not just code.)
3. "Write suggest() using a deletion index, and add a unit test that proves a word two
   substitutions away is found." (Ties the implementation to a verifying test.)

## Bad AI prompts

1. "Why do the tests fail?" without pasting the failing assertion. (The agent has to guess
   which test.)
2. "Implement a spell checker." (Ignores the Dictionary class and its normalization rules;
   you get a second normalizer that disagrees with the first.)
3. "Use a trie" as the first optimization. (A trie helps with prefixes; edit distance
   search over a trie is a lot of code for a 50 minute slot and does not beat the
   deletion index here.)
