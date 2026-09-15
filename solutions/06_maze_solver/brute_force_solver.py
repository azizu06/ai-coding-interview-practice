"""Brute force: depth-first search that keeps the best known distance per
(cell, keys) state and revisits whenever it finds a shorter one.

Correct, and fine on corridor mazes, but on open fields it re-walks the
same cells enormous numbers of times. Passes the small and medium timed
tests, fails large and huge.
"""


class Solver:
    def __init__(self, maze):
        self.maze = maze

    def shortest_path(self):
        maze = self.maze
        goal = maze.exit
        best = {}
        answer = -1
        stack = [(maze.start[0], maze.start[1], frozenset(), 0)]
        while stack:
            r, c, keys, dist = stack.pop()
            if best.get((r, c, keys), dist) < dist:
                continue
            if (r, c) == goal:
                if answer == -1 or dist < answer:
                    answer = dist
                continue
            if answer != -1 and dist + 1 >= answer:
                continue
            for nr, nc in maze.neighbors(r, c, keys):
                key = maze.key_at(nr, nc)
                new_keys = keys | {key} if key else keys
                nd = dist + 1
                state = (nr, nc, new_keys)
                if best.get(state, nd + 1) <= nd:
                    continue
                best[state] = nd
                stack.append((nr, nc, new_keys, nd))
        return answer
