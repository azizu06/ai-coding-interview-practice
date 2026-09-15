"""Generate the committed traffic files. Run: python gen_data.py

Only the small log lives on disk. The bigger logs used by the timed tests are
rebuilt in memory by src/traffic_data.py from the same generator and their own
seeds, because as text they would be many megabytes.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from traffic_data import generate  # noqa: E402


def write(name, lines):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"{name}: {len(lines)} lines, {os.path.getsize(path)} bytes")


def main():
    limits, requests = generate(300, 4000, 60000, (4, 4, 2, 0), seed=100001)
    write("limits_small.txt", limits)
    write("requests_small.txt", requests)


if __name__ == "__main__":
    main()
