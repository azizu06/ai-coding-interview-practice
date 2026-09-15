# 08 Card Game

Difficulty: Medium

## Problem

Players are dealt seven cards and score the best five of them. Your job is to
work out the score of a hand.

The rules of the game live in `src/deck.py`. Read them. One of them is not the
rule you are used to: in this game a FLUSH BEATS A FULL HOUSE. Do not let an
assistant fill in a poker table from memory.

A score is a pair `(category, tiebreakers)`. The category is a number from 0
(high card) to 8 (straight flush). The tiebreakers are a tuple of rank values
ordered so that plain tuple comparison ranks two scores correctly, so
`score_a > score_b` means hand A wins.

## Example

```
hand:  Ks Qs Js Ts 9s Kd Kc
score: (8, (13,))
```

The three kings look promising, but five of the seven cards are spades running
nine to king, so the best five cards make a straight flush with a king high.

```
hand:  As Ks 9s 4s 7h 2d 3c
score: (0, (14, 13, 9, 7, 4))
```

Four spades are not a flush. Nothing else lines up, so this is a high card
hand.

## Files

```
data/hands_small.txt   100 hands, one per line
data/hands_medium.txt  5000 hands
data/gen_data.py       the script that produced the files above
src/deck.py            the card rules and the parser (read this first)
src/hand_data.py       loaders, and the builders for the three big hand sets
src/main.py            runnable demo
src/solver.py          the Solver stub you complete
src/test_deck.py       unit tests for Deck
src/test_solver.py     unit tests for Solver, correctness first, then timed
```

The three largest hand sets are not committed, since they would be megabytes of
text. `src/hand_data.py` rebuilds them from fixed seeds: 60000 ordinary hands,
250000 ordinary hands, and 60000 hands rigged so that flushes and straights
turn up far more often than chance.

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `Deck` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `best_hand()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as
you would in the real interview. Start a 50 minute timer.
