# 07 Friend Recommender: answer key

## The two bugs in `SocialGraph`

1. `add_friendship` builds the `edge` tuple and adds it to `self._known`, but
   it never checks whether the edge was already there. The docstring promises
   that adding the same friendship twice changes nothing, so the guard is
   missing. Every repeated pair appends another copy to both friend lists,
   which inflates degrees and double counts shared friends. Fix:

   ```python
   if edge in self._known:
       return
   self._known.add(edge)
   ```

   Caught by `test_duplicate_friendship_is_ignored` and
   `test_repeats_do_not_inflate_degree`.
2. `friends_of` uses `self._friends[user]`, which raises `KeyError` for a user
   who never appeared in a friendship. The class docstring says an unseen user
   simply has no friends. Fix: `return self._friends.get(user, [])`. This also
   repairs `degree`, which is written in terms of `friends_of`. Caught by
   `test_unknown_user_has_no_friends` and `test_degree_of_unknown_user_is_zero`,
   and visible in `main.py`, which asks for the friends of user 404.

Filled-in `????` values live in `expected.json` in this folder.

## Brute force

`brute_force_solver.py` walks every user in the graph for every query and
intersects friend lists. Cost per query is `O(N log N)` to build the sorted
user list plus `O(N * d)` for the intersections.

It passes the 200 user and 2000 user timed tests (17 ms on medium). It needs
about 6.2 s on the 50000 user graph and about 5.1 s on the dense graph, against
budgets of 1.0 s and 1.5 s.

## Optimization ladder

### Rung 1: scan every user per query

The brute force above. Breaks on `test_large_50000_users`: the work per query
is proportional to the size of the whole graph, even though only a few hundred
users can possibly share a friend with the query user.

### Rung 2: friends of friends, filtered against the friend list

Walk the user's friends, walk their friends, count. That drops the candidate
set from N to at most `d^2`. The natural way to drop people who are already
friends is `if candidate in graph.friends_of(user): continue`, because
`friends_of` is what the class hands you.

That test is a linear scan of a list. On a sparse graph nobody notices. On the
dense graph there are thousands of candidates per query and each one scans a
150 entry list, so the filter costs `O(candidates * d)` and swamps the counting.

Cost: `O(d^2 + candidates * d)` per query. Passes small, medium and large.
Breaks on `test_dense_150_friends_each`: about 2.1 s against a 1.5 s budget.
See `fof_list_solver.py`.

### Rung 3: hoist the friend set, count in C, take the top k with a heap

Three changes, in order of how much they matter:

* build `set(graph.friends_of(user))` once per query, so the filter is `O(1)`
  per candidate instead of `O(d)`
* count with `Counter.update(graph.friends_of(friend))`, which counts a whole
  friend list inside CPython rather than one `dict.get` per element
* take the top `limit` with `heapq.nsmallest` on `(-shared, candidate)` instead
  of sorting every candidate

Cost: `O(d^2 + candidates)` per query. About 0.41 s on the dense graph and 7 ms
on the large graph. Reference: `solver.py`.

## Timed test summary (measured on this machine)

| test | graph | budget | brute | rung 2 | reference |
| --- | --- | --- | --- | --- | --- |
| small | 200 users, 30 queries | 1.0 s | 0.00 s | 0.00 s | 0.00 s |
| medium | 2000 users, 60 queries | 1.0 s | 0.02 s | 0.00 s | 0.00 s |
| large | 50000 users, 500 queries | 1.0 s | 6.2 s | 0.01 s | 0.01 s |
| dense | 8000 users x 150 friends, 400 queries | 1.5 s | 5.1 s | 2.1 s | 0.41 s |

## Good AI prompts

1. "Read social_graph.py and list every promise the class docstring makes, then
   show me the line that enforces each one. Which promise has no line?"
2. "Here is my recommend(). On a graph with 8000 users and 150 friends each it
   takes 2.1 s for 400 queries, but on 50000 users with 10 friends each it takes
   0.01 s for 500 queries. Which line has a cost that depends on both the
   candidate count and the degree?"
3. "Rewrite this candidate loop so that excluding existing friends is a constant
   time test, and take only the top 10 without sorting every candidate."

## Bad AI prompts

1. "Fix the bugs in social_graph.py." (No contract to check against, so the
   agent guesses and may rewrite the insertion order behaviour the tests rely on.)
2. "Make the dense test pass." (Invites raising the budget or trimming the
   candidate set in a way that changes the answer.)
3. "Optimize my friend recommender." (You get micro-tweaks to the counting loop
   rather than the one line that costs O(candidates * degree).)
