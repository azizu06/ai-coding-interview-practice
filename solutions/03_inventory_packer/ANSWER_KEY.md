# 03 Inventory Packer: answer key

## The two bugs in `Inventory`

1. `add_item` accepts a weight of zero. The guard reads `weight < 0`, but an item that
   weighs nothing is not an item: the commented-out `test_rejects_zero_weight` asserts the
   inventory is still empty after one is added, and `test_constructor_skips_invalid_pairs`
   counts a `("ghost", 0)` pair out. Fix: `weight <= 0`. `main.py` prints `True` for the
   zero-weight "ghost" item, which is the same failure without running a test.
2. `items_by_weight` orders equal weights by name descending. It sorts on
   `(weight, name)` with `reverse=True`, which reverses the name order along with the
   weight order. Fix: sort on `(-weight, name)` without `reverse`.
   `test_equal_weights_are_ordered_by_name` and `test_heaviest_breaks_ties_by_name`
   expose it.

## Expected values for the `????` tests

See `expected.json`. Box counts: example 4, small 6, medium 618, large 12211,
huge 60999, wide 7044. First-fit decreasing and best-fit decreasing give the same counts
on every file here, and each count equals the `ceil(total / capacity)` lower bound or is
one above it.

## Brute force

First-fit decreasing with a linear scan over every open box for every item. With N items
and B boxes that is O(N * B), and B grows with N, so it is quadratic in practice: 2000
items take 12 ms, 40000 items take about 5 s (budget 1 s). See `brute_force_solver.py`.

## Optimization ladder

| Rung | Idea | Complexity | Passes | Breaks on |
| --- | --- | --- | --- | --- |
| 1 | First-fit decreasing, scan every open box | O(N * B) | medium | large (5 s), huge, wide |
| 2 | Group open boxes by remaining room in a dict keyed by room, and for each item scan room values from `weight` up to `capacity` for a non-empty group | O(N * C) worst case | medium, large, huge (0.26 s) | wide: capacity 100000 means each new box costs a scan of tens of thousands of empty room values, about 14 s total |
| 3 | Same grouping, plus a sorted list of the distinct non-empty room values so the tightest fitting group is one `bisect_left` away | O(N * (log C + D)) where D is the number of distinct room values, and the list edits are C-speed memmoves | everything (200000 items in 0.09 s, wide in 0.01 s) | |

Rung 3 is the reference in `solver.py`. Picking the tightest group is best-fit decreasing;
it produces the same box counts as first-fit decreasing on these files and is never worse
than the accepted bound in the tests.

## Good AI prompts

1. "test_equal_weights_are_ordered_by_name says items of equal weight come back ordered by
   name. Show me the sort call in items_by_weight and explain what reverse=True does to the
   second element of the sort key." (Names the invariant and the suspicious line.)
2. "My first-fit decreasing scans every open box per item and takes 5 s on 40000 items.
   Boxes only differ by how much room is left. Propose a structure keyed by remaining room
   and tell me its cost per item when capacity is 100 and when it is 100000." (Forces the
   agent to reason about both timed cases.)
3. "Write a check that every item name appears exactly once across the boxes and no box
   exceeds capacity, then run it on the 200000 item set." (Verification before speed.)

## Bad AI prompts

1. "Solve bin packing optimally." (NP-hard; the agent will produce something exponential
   or a long explanation. The tests want first-fit decreasing quality, not optimality.)
2. "Make pack faster" with no timing numbers. (You get micro-optimizations of the scan.)
3. "Rewrite Inventory." (The bugs are two characters; a rewrite risks changing the
   ordering contract the solver relies on.)
