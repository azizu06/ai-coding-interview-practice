"""Read this first."""

KEY_LETTERS = "abcdef"
DOOR_LETTERS = "ABCDEF"

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


class Maze:
    WALL = "#"
    FLOOR = "."
    START = "S"
    EXIT = "G"

    def __init__(self, rows):
        if not rows:
            raise ValueError("maze needs at least one row")
        width = len(rows[0])
        for line in rows:
            if len(line) != width:
                raise ValueError("all rows must have the same length")
        self.grid = [list(line) for line in rows]
        self.rows = len(rows)
        self.cols = width
        self.start = None
        self.exit = None
        self.keys = {}
        self.doors = {}
        for r, line in enumerate(rows):
            for c, ch in enumerate(line):
                if ch == self.START:
                    self.start = (r, c)
                elif ch == self.EXIT:
                    self.exit = (r, c)
                elif ch in KEY_LETTERS:
                    self.keys[ch] = (r, c)
                elif ch in DOOR_LETTERS:
                    self.doors.setdefault(ch, []).append((r, c))
        if self.start is None or self.exit is None:
            raise ValueError("maze needs exactly one S and one G")

    @classmethod
    def parse(cls, text):
        rows = [line.rstrip("\r") for line in text.split("\n")]
        rows = [line for line in rows if line.strip()]
        return cls(rows)

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def cell(self, r, c):
        return self.grid[r][c]

    def key_at(self, r, c):
        ch = self.grid[r][c]
        return ch if ch in KEY_LETTERS else None

    def all_keys(self):
        return sorted(self.keys)

    def is_open(self, r, c, keys=frozenset()):
        if not self.in_bounds(r, c):
            return False
        ch = self.grid[r][c]
        if ch == self.WALL:
            return False
        if ch in DOOR_LETTERS:
            return ch in keys
        return True

    def neighbors(self, r, c, keys=frozenset()):
        result = []
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols - 1:
                if self.is_open(nr, nc, keys):
                    result.append((nr, nc))
        return result

    def __str__(self):
        return "\n".join("".join(line) for line in self.grid)
