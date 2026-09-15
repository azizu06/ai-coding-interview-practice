# 08 Card Game

*Score the best five of seven cards under house rules where a flush beats a full house.*

|  |  |
| --- | --- |
| **Difficulty** | Medium |
| **Files you edit** | `src/deck.py`, `src/solver.py` |
| **Suggested time** | 50 min |

## The problem

Players are dealt seven cards and score the best five of them. Your job is to work out the
score of a hand.

A card is written as two characters, a rank then a suit.

```
ranks  2 3 4 5 6 7 8 9 T J Q K A   (T is the ten, A is high)
suits  c d h s                     (clubs diamonds hearts spades)
```

So `Ah` is the ace of hearts and `Td` is the ten of diamonds. Suits have no strength of
their own, and they only decide flushes.

The nine categories run weakest first from 0 to 8.

```
0 high card    1 one pair   2 two pair        3 three of a kind   4 straight
5 full house   6 flush      7 four of a kind  8 straight flush
```

In this game a FLUSH BEATS A FULL HOUSE.

A straight is five ranks in a row. The ace plays both high, T J Q K A, and low, A 2 3 4 5.
The low one is called the wheel, and its high card counts as 5, so it is the weakest
straight.

A score is a pair `(category, tiebreakers)`. The tiebreakers are a tuple of rank values
ordered so that plain tuple comparison ranks two scores correctly, so `score_a > score_b`
means hand A wins.

```
hand:  Ks Qs Js Ts 9s Kd Kc
score: (8, (13,))
```

The three kings look promising, but five of the seven cards are spades running nine to
king, so the best five cards make a straight flush with a king high.

```
hand:  As Ks 9s 4s 7h 2d 3c
score: (0, (14, 13, 9, 7, 4))
```

Four spades are not a flush. Nothing else lines up, so this is a high card hand.

## The codebase

| File | What it holds |
| --- | --- |
| `data/hands_small.txt` | 100 hands, one per line |
| `data/hands_medium.txt` | 5000 hands |
| `data/gen_data.py` | the script that produced the files above |
| `src/main.py` | runnable demo |
| `src/deck.py` | the card parser and the flush and straight helpers |
| `src/hand_data.py` | loaders, and the builders for the three big hand sets |
| `src/solver.py` | the Solver stub you complete |
| `src/test_deck.py` | unit tests for Deck |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

The three largest hand sets are not committed, since they would be megabytes of text.
`src/hand_data.py` rebuilds them from fixed seeds: 60000 hands, 250000 hands, and a third
set of 60000 hands dealt from a different mix.

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `Deck` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `best_hand()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/08_card_game/src/main.py
python -m unittest discover -s problems/08_card_game/src -v
```

From inside `problems/08_card_game/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_deck -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

---

Spoilers ahead: [`../../solutions/08_card_game/ANSWER_KEY.md`](../../solutions/08_card_game/ANSWER_KEY.md).
Do not open it until your timer is done.
