"""Reference solution: compress the grid to points of interest, then run
Dijkstra over (point, key mask) states.

Points of interest are S, E, every key and every door. One BFS from each
point (stopping at other points) gives the walking distance between them
while ignoring key rules. The key rules are then applied on the tiny graph:
a door edge may be taken only when the mask holds its key, and landing on a
key adds it to the mask.

Cost: P BFS runs over the grid plus Dijkstra over P * 2^K states, where
P = 2 + keys + doors. The alternative, BFS over (cell, mask) states, costs
cells * 2^K and dies on the 300x300 maze with six keys in the open.
"""

import heapq
from collections import deque

from maze import DOOR_LETTERS, KEY_LETTERS


class Solver:
    def __init__(self, maze):
        self.maze = maze

    def shortest_path(self):
        maze = self.maze
        rows, cols = maze.rows, maze.cols
        wall = maze.WALL
        grid = [maze.cell(r, c) for r in range(rows) for c in range(cols)]
        n = rows * cols

        adjacency = [()] * n
        for idx in range(n):
            if grid[idx] == wall:
                continue
            r, c = divmod(idx, cols)
            cells = []
            if r > 0 and grid[idx - cols] != wall:
                cells.append(idx - cols)
            if r < rows - 1 and grid[idx + cols] != wall:
                cells.append(idx + cols)
            if c > 0 and grid[idx - 1] != wall:
                cells.append(idx - 1)
            if c < cols - 1 and grid[idx + 1] != wall:
                cells.append(idx + 1)
            adjacency[idx] = tuple(cells)

        keys = maze.all_keys()
        bit = {key: 1 << i for i, key in enumerate(keys)}
        start = maze.start[0] * cols + maze.start[1]
        goal = maze.exit[0] * cols + maze.exit[1]
        points = [start, goal]
        for idx, ch in enumerate(grid):
            if ch in KEY_LETTERS or ch in DOOR_LETTERS:
                points.append(idx)
        point_index = {cell: i for i, cell in enumerate(points)}

        edges = [[] for _ in points]
        for src_i, src in enumerate(points):
            dist = [-1] * n
            dist[src] = 0
            queue = deque([src])
            while queue:
                cur = queue.popleft()
                d = dist[cur] + 1
                for nb in adjacency[cur]:
                    if dist[nb] != -1:
                        continue
                    dist[nb] = d
                    other = point_index.get(nb)
                    if other is None:
                        queue.append(nb)
                    else:
                        edges[src_i].append((other, d))

        best = {(0, 0): 0}
        heap = [(0, 0, 0)]
        while heap:
            d, p, mask = heapq.heappop(heap)
            if p == 1:
                return d
            if best.get((p, mask), d) < d:
                continue
            for q, w in edges[p]:
                ch = grid[points[q]]
                if ch in DOOR_LETTERS:
                    if not mask & bit.get(ch.lower(), 0):
                        continue
                    new_mask = mask
                elif ch in KEY_LETTERS:
                    new_mask = mask | bit[ch]
                else:
                    new_mask = mask
                nd = d + w
                state = (q, new_mask)
                if nd < best.get(state, nd + 1):
                    best[state] = nd
                    heapq.heappush(heap, (nd, q, new_mask))
        return -1
