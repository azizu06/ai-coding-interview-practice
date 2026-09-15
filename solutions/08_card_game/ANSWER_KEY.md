# 08 Card Game: answer key

## The two bugs in `Deck`

1. `flush_suit` returns a suit once it sees four cards of it: `if count >= 4`.
   The docstring says five or more. With the bug, more than half of all seven
   card hands are reported as flushes, and the tiebreaker tuple only has four
   ranks in it. Fix: `if count >= 5`. Caught by
   `test_four_of_a_suit_is_not_a_flush` and
   `test_four_and_three_is_still_not_a_flush`, and again in the solver tests by
   `test_four_of_a_suit_is_only_a_high_card`.
2. `straight_high` never handles the wheel. It sorts the distinct ranks and
   looks for a run of five, which finds every straight except A 2 3 4 5, since
   the ace sorts as 14 rather than 1. The class docstring says the wheel is a
   straight with a high card of 5. Fix, after the run loop:

   ```python
   if best == 0 and {14, 2, 3, 4, 5}.issubset(distinct):
       best = 5
   ```

   Caught by `test_the_wheel_is_a_straight`,
   `test_the_wheel_inside_seven_ranks` and
   `test_the_wheel_counts_as_a_straight`.

Filled-in `????` values live in `expected.json` in this folder.

Worth noting for anyone leaning on an assistant: this game scores a flush above
a full house. A generated evaluator will almost always get that backwards, and
the category totals in the timed tests will be off by exactly the number of
flushes and full houses in the file.

## Brute force

`brute_force_solver.py` walks all 21 five card subsets of the seven cards with
`itertools.combinations` and scores each one from scratch with `Counter` and
`sorted`. Cost is 21 full scorings per hand.

It passes the 100 hand and 5000 hand tests (0.19 s on medium) and fails
everything above: 2.2 s on the 60000 hand files against a 1.5 s budget, and
9.2 s on the 250000 hand file.

## Optimization ladder

### Rung 1: all 21 subsets, scored from scratch

The brute force above. Breaks on `test_large_60000_hands` and
`test_rich_60000_flushy_hands`.

### Rung 2: all 21 subsets, scored with a fast scorer

The tempting next move is to keep the enumeration and speed up the scorer:
replace `Counter` with a 15 slot count array, replace the sort with a rank
bitmask, and precompute a straight table indexed by that bitmask, so a straight
lookup is one list index.

That is about three times faster. Cost per hand is still 21 scorings.

Passes small, medium, large and rich. Breaks on `test_huge_250000_hands`: about
4.5 s against a 1.5 s budget. See `fast_combo_solver.py`.

### Rung 3: stop enumerating, read the seven cards

The seven cards already say which five are best. Count how many of each rank
and each suit are present, then walk the categories from the top:

* five or more of one suit plus a straight among those suits is a straight flush
* a rank with four cards is four of a kind
* five or more of one suit is a flush (which outranks a full house here)
* a triple plus another triple or a pair is a full house
* a straight among all seven ranks is a straight
* and so on down to high card

One pass over seven cards, one straight lookup, no subsets. Add the precomputed
straight table from rung 2 and the hot loop never sorts anything.

Cost: `O(1)` per hand with a small constant. About 0.36 s on the 250000 hand
file. Reference: `solver.py`.

A useful halfway point is in `direct_seven_solver.py`: the same seven card logic
but with `Counter`, `sorted` and an uncached `Deck.straight_high`. It passes
every timed test at about 0.66 s on huge, which shows that dropping the
enumeration is what mattered and the table is the polish.

## Timed test summary (measured on this machine)

| test | hands | budget | brute | rung 2 | reference |
| --- | --- | --- | --- | --- | --- |
| small | 100 | 1.0 s | 0.00 s | 0.00 s | 0.00 s |
| medium | 5000 | 1.0 s | 0.19 s | 0.09 s | 0.01 s |
| large | 60000 | 1.5 s | 2.23 s | 1.08 s | 0.09 s |
| rich | 60000 flushy | 1.5 s | 2.20 s | 1.10 s | 0.08 s |
| huge | 250000 | 1.5 s | 9.25 s | 4.49 s | 0.36 s |

## Good AI prompts

1. "Read deck.py and write down the rules of this game in your own words,
   including anything that differs from standard poker. Do not use anything you
   already know about poker hand rankings."
2. "Given seven cards, prove that I never need to look at the 21 five card
   subsets: for each category, show which five of the seven are forced."
3. "My evaluator spends most of its time in straight_high, which sorts a set on
   every call. The only input that matters is which of the 13 ranks are present.
   Turn that into a lookup keyed on a 13 bit mask."

## Bad AI prompts

1. "Write a poker hand evaluator." (You get the standard ranking, so flushes and
   full houses come out swapped and every category total is wrong.)
2. "Speed up score_five." (The scorer was never the problem; calling it 21 times
   per hand was.)
3. "Fix the bugs in deck.py." (No contract in the prompt, so the agent may
   decide four to a flush is intentional or that the ace should not play low.)
