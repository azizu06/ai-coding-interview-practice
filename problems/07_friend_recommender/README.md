# 07 Friend Recommender

*Rank the people a user might know by how many friends they already share.*

|  |  |
| --- | --- |
| **Difficulty** | Medium |
| **Files you edit** | `src/social_graph.py`, `src/solver.py` |
| **Suggested time** | 50 min |

## The problem

You are given a social graph. Friendships are mutual. For a given user, suggest people they
might know: users who share at least one friend with them but are not already their friend.

Candidates are ranked by how many friends they share with the user, highest count first.
When two candidates share the same number of friends, the smaller user id comes first. The
user themself is never a candidate, and neither is anyone already on their friend list.

The `SocialGraph` class in `src/social_graph.py` stores the friendships. The `Solver` class
in `src/solver.py` is where the ranking goes.

Friendships:

```
1-2  1-3  1-4  2-5  3-5  4-5  2-6  3-6  5-7  6-7  7-8
```

`Solver(graph).recommend(1, 5)` returns:

```
[(5, 3), (6, 2)]
```

User 5 is a friend of 2, 3 and 4, all three of whom are friends of user 1, so they share
three friends. User 6 is a friend of 2 and 3, so they share two. User 7 shares nobody with
user 1 and is not suggested. A user with no friends gets an empty list.

## The codebase

| File | What it holds |
| --- | --- |
| `data/friends_small.txt` | 200 users, about 4 friends each |
| `data/friends_medium.txt` | 2000 users, about 8 friends each |
| `data/queries_small.txt` | the users to recommend for |
| `data/queries_medium.txt` | the users to recommend for |
| `data/gen_data.py` | the script that produced the files above |
| `src/main.py` | runnable demo |
| `src/social_graph.py` | the SocialGraph class, read this first |
| `src/graph_data.py` | loaders, and the builders for the two big graphs |
| `src/solver.py` | the Solver stub you complete |
| `src/test_social_graph.py` | unit tests for SocialGraph |
| `src/test_solver.py` | unit tests for Solver, correctness first, then timed |

The two largest graphs are not committed. They would be several megabytes of text, so
`src/graph_data.py` rebuilds them from a fixed seed: 50000 users with about 10 friends each,
and 20000 users with about 150 friends each.

## Your tasks

The six steps below map onto the four phases of the interview.

1. **Comprehension.** Explore the code and work out how the existing pieces fit together.
2. **Comprehension.** Run the demo: `python src/main.py`.
3. **Comprehension.** Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. **Bugs.** Fix the bugs. The `SocialGraph` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. **Implementation.** Implement the Solver. Complete `recommend()` in `src/solver.py`.
6. **Optimization.** Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.

## How to run

If you copied this folder out of the repository on its own, use the commands that run from inside `src`.

From the repository root:

```bash
python problems/07_friend_recommender/src/main.py
python -m unittest discover -s problems/07_friend_recommender/src -v
```

From inside `problems/07_friend_recommender/src`:

```bash
python main.py
python -m unittest discover -s . -v
python -m unittest test_social_graph -v
```

Until you implement the solver, `test_solver.py` fails and the domain tests pass. That is
the shipped state, not a broken checkout.

---

Spoilers ahead: [`../../solutions/07_friend_recommender/ANSWER_KEY.md`](../../solutions/07_friend_recommender/ANSWER_KEY.md).
Do not open it until your timer is done.
