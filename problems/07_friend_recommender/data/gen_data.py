"""Generate the committed friendship files. Run: python gen_data.py

Only the small and medium graphs live on disk. The large and dense graphs used
by the timed tests would be several megabytes of text, so src/graph_data.py
rebuilds them in memory from the same seeds instead.

Every graph is a ring of near neighbours plus a batch of random extra edges,
which gives a few shared friends between most pairs of nearby users.
"""

import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))


def build_pairs(user_count, degree, seed):
    rng = random.Random(seed)
    pairs = []
    ring = max(1, degree // 4)
    for user in range(user_count):
        for step in range(1, ring + 1):
            pairs.append((user, (user + step) % user_count))
    extra = user_count * (degree - 2 * ring) // 2
    for _ in range(max(0, extra)):
        a = rng.randrange(user_count)
        b = rng.randrange(user_count)
        if a != b:
            pairs.append((a, b))
    return pairs


def pick_queries(user_count, count, seed):
    rng = random.Random(seed)
    return [rng.randrange(user_count) for _ in range(count)]


def write_pairs(name, pairs):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(f"{a} {b}" for a, b in pairs) + "\n")
    print(f"{name}: {len(pairs)} lines, {os.path.getsize(path)} bytes")


def write_ids(name, ids):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(str(i) for i in ids) + "\n")
    print(f"{name}: {len(ids)} lines, {os.path.getsize(path)} bytes")


def main():
    write_pairs("friends_small.txt", build_pairs(200, 4, seed=70010))
    write_ids("queries_small.txt", pick_queries(200, 30, seed=70011))
    write_pairs("friends_medium.txt", build_pairs(2000, 8, seed=70012))
    write_ids("queries_medium.txt", pick_queries(2000, 60, seed=70013))


if __name__ == "__main__":
    main()
