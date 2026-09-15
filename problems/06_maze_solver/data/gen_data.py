"""Regenerate the maze data files. Deterministic: python data/gen_data.py

Layout of every generated maze:
  * random walls on an open field (wall density differs per size)
  * S in the top left area
  * a vault in the bottom right holding G, entered through a corridor of
    doors, one per key
  * keys either lying in the open (scattered=True) or each placed inside a
    small room behind a door (scattered=False)
"""

import os
import random
from collections import deque

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_LETTERS = "abcdef"


def blank_field(rows, cols, density, rng):
    grid = [["#"] * cols for _ in range(rows)]
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            grid[r][c] = "#" if rng.random() < density else "."
    return grid


def carve_vault(grid, r0, c0, keys):
    """5 rows by (len(keys) + 5) cols. Doors A.. in order, then a 3x3 room with G."""
    k = len(keys)
    for r in range(r0, r0 + 5):
        for c in range(c0, c0 + k + 5):
            grid[r][c] = "#"
    for r in range(r0 + 1, r0 + 4):
        for c in range(c0 + k + 1, c0 + k + 4):
            grid[r][c] = "."
    grid[r0 + 2][c0 + k + 2] = "G"
    for i, key in enumerate(keys):
        grid[r0 + 2][c0 + 1 + i] = key.upper()
    grid[r0 + 2][c0] = "."
    grid[r0 + 2][c0 - 1] = "."


def carve_room(grid, r0, c0, key, door_key):
    """5x5 room, key in the middle, door in the top wall (or an opening)."""
    for r in range(r0, r0 + 5):
        for c in range(c0, c0 + 5):
            grid[r][c] = "#"
    for r in range(r0 + 1, r0 + 4):
        for c in range(c0 + 1, c0 + 4):
            grid[r][c] = "."
    grid[r0 + 2][c0 + 2] = key
    grid[r0][c0 + 2] = door_key.upper() if door_key else "."
    grid[r0 - 1][c0 + 2] = "."


def overlaps(box, boxes):
    r0, c0, r1, c1 = box
    for a0, b0, a1, b1 in boxes:
        if r0 <= a1 and a0 <= r1 and c0 <= b1 and b0 <= c1:
            return True
    return False


def reachable_ignoring_doors(grid, start):
    rows, cols = len(grid), len(grid[0])
    seen = {start}
    dq = deque([start])
    while dq:
        r, c = dq.popleft()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                if (nr, nc) not in seen:
                    seen.add((nr, nc))
                    dq.append((nr, nc))
    return seen


def make_maze(rows, cols, n_keys, density, seed, scattered):
    keys = KEY_LETTERS[:n_keys]
    for attempt in range(1000):
        rng = random.Random(seed * 1000 + attempt)
        grid = blank_field(rows, cols, density, rng)
        boxes = []
        start = (1, 1)
        grid[1][1] = "S"
        grid[1][2] = "."
        grid[2][1] = "."
        boxes.append((0, 0, 3, 3))
        vr, vc = rows - 6, cols - (n_keys + 6)
        carve_vault(grid, vr, vc, keys)
        boxes.append((vr - 1, vc - 2, vr + 5, cols - 1))
        placed = True
        for i, key in enumerate(keys):
            for _ in range(200):
                if scattered:
                    r = rng.randrange(2, rows - 2)
                    c = rng.randrange(2, cols - 2)
                    box = (r - 1, c - 1, r + 1, c + 1)
                    if overlaps(box, boxes):
                        continue
                    grid[r][c] = key
                    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                        grid[nr][nc] = "."
                    boxes.append(box)
                    break
                r = rng.randrange(3, rows - 6)
                c = rng.randrange(2, cols - 6)
                box = (r - 2, c - 1, r + 5, c + 5)
                if overlaps(box, boxes):
                    continue
                carve_room(grid, r, c, key, keys[i - 1] if i > 0 else None)
                boxes.append(box)
                break
            else:
                placed = False
                break
        if not placed:
            continue
        seen = reachable_ignoring_doors(grid, start)
        targets = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] in keys or grid[r][c] == "G"]
        if all(t in seen for t in targets):
            return "\n".join("".join(line) for line in grid) + "\n"
    raise RuntimeError("could not generate a connected maze")


SPECS = {
    "maze_small.txt": dict(rows=20, cols=20, n_keys=1, density=0.30, seed=6, scattered=True),
    "maze_medium.txt": dict(rows=30, cols=30, n_keys=2, density=0.42, seed=7, scattered=False),
    "maze_large.txt": dict(rows=120, cols=120, n_keys=3, density=0.30, seed=8, scattered=False),
    "maze_huge.txt": dict(rows=300, cols=300, n_keys=6, density=0.25, seed=9, scattered=True),
}


def main():
    for name, spec in SPECS.items():
        text = make_maze(**spec)
        with open(os.path.join(DATA_DIR, name), "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"wrote {name}: {spec['rows']}x{spec['cols']}, {spec['n_keys']} keys")


if __name__ == "__main__":
    main()
