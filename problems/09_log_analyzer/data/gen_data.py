"""Generate the committed log file. Run: python gen_data.py

Only the small log lives on disk. The three bigger logs used by the timed tests
are rebuilt in memory by src/log_data.py from the same generator and their own
seeds, because as text they would be tens of megabytes.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from log_data import generate_lines  # noqa: E402


def write(name, lines):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"{name}: {len(lines)} lines, {os.path.getsize(path)} bytes")


def main():
    write("log_small.txt", generate_lines(2000, 600, seed=90001))


if __name__ == "__main__":
    main()
