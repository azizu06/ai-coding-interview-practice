"""Middle rung: BFS over (cell, keys) states, built straight on top of the
Maze API. Correct, passes small/medium/large, fails the huge maze because
six keys in the open means up to 64 states per cell.
"""

from collections import deque


class Solver:
    def __init__(self, maze):
        self.maze = maze

    def shortest_path(self):
        maze = self.maze
        goal = maze.exit
        start = (maze.start[0], maze.start[1], frozenset())
        seen = {start}
        queue = deque([(start, 0)])
        while queue:
            (r, c, keys), dist = queue.popleft()
            if (r, c) == goal:
                return dist
            for nr, nc in maze.neighbors(r, c, keys):
                key = maze.key_at(nr, nc)
                new_keys = keys | {key} if key else keys
                state = (nr, nc, new_keys)
                if state not in seen:
                    seen.add(state)
                    queue.append((state, dist + 1))
        return -1
