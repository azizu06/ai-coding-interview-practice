import os
import random

from social_graph import SocialGraph

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

EXAMPLE_PAIRS = [
    (1, 2), (1, 3), (1, 4),
    (2, 5), (3, 5), (4, 5),
    (2, 6), (3, 6),
    (5, 7), (6, 7),
    (7, 8),
]

_CACHE = {}


def _read_pairs(name):
    path = os.path.join(DATA_DIR, name)
    pairs = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            a, b = line.split()
            pairs.append((int(a), int(b)))
    return pairs


def _read_ids(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, encoding="utf-8") as handle:
        return [int(line) for line in handle if line.strip()]


def _build_pairs(user_count, degree, seed):
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


def _cached(key, factory):
    if key not in _CACHE:
        _CACHE[key] = factory()
    return _CACHE[key]


def _queries(user_count, count, seed):
    rng = random.Random(seed)
    return [rng.randrange(user_count) for _ in range(count)]


def get_example_graph():
    return SocialGraph(EXAMPLE_PAIRS)


def get_small_graph():
    return _cached("small", lambda: SocialGraph(_read_pairs("friends_small.txt")))


def get_small_queries():
    return _read_ids("queries_small.txt")


def get_medium_graph():
    return _cached("medium", lambda: SocialGraph(_read_pairs("friends_medium.txt")))


def get_medium_queries():
    return _read_ids("queries_medium.txt")


def get_large_graph():
    return _cached("large", lambda: SocialGraph(_build_pairs(50000, 10, seed=70001)))


def get_large_queries():
    return _queries(50000, 500, seed=70002)


def get_dense_graph():
    return _cached("dense", lambda: SocialGraph(_build_pairs(20000, 150, seed=70003)))


def get_dense_queries():
    return _queries(20000, 400, seed=70004)
