# 03 Inventory Packer

Difficulty: Easy

## Problem

A warehouse has a pile of items, each with an integer weight, and an unlimited supply of
identical boxes that hold at most `capacity` weight. Pack every item into boxes using as
few boxes as you reasonably can.

Finding the true minimum is hard in general, so the tests accept any valid packing that
uses no more boxes than the classic "first-fit decreasing" strategy: sort items heaviest
first, and drop each one into the first box that has room, opening a new box when none does.

The `Inventory` class in `src/inventory.py` stores items and hands them back sorted. The
`Solver` class in `src/solver.py` does the packing.

## Example

Items (capacity 10):

```
anvil 9, book 3, cup 3, dish 4, egg 1, fan 6, globe 5
```

Total weight 31, so at least 4 boxes. One valid answer with 4 boxes:

```
box 1: anvil, egg          (10)
box 2: fan, dish           (10)
box 3: globe, book         (8)
box 4: cup                 (3)
```

An item heavier than the capacity cannot be packed; `pack` raises `ValueError`.

## Files

```
data/items_small.txt      12 items
data/items_medium.txt     2000 items, weights 1 to 60
data/items_large.txt      40000 items, weights 1 to 60
data/items_wide.txt       20000 items, weights 1 to 70000 (capacity 100000)
data/gen_data.py          the script that produced the files above
src/main.py               runnable demo
src/inventory.py          the Inventory class (read this first)
src/items.py              loaders, plus the in-memory generator for the 200000 item set
src/solver.py             the Solver stub you complete
src/test_inventory.py     unit tests for Inventory
src/test_solver.py        unit tests for Solver, correctness first, then timed
```

## Your Tasks

1. Explore the code. Figure out how the existing code works.
2. Run `python src/main.py`.
3. Run the unit tests: `python -m unittest discover -s src -v`. Some tests are commented out; uncomment them.
4. Fix the bugs. The `Inventory` class has two bugs. Commented-out tests use `????` as expected values. Figure out what they should be and make the tests pass.
5. Implement the Solver. Complete `pack()` in `src/solver.py`.
6. Optimize. Uncomment the timed tests in `src/test_solver.py` and make them pass.

This is an AI-assisted problem. Use your coding agent as much or as little as you would in
the real interview. Start a 50 minute timer.
