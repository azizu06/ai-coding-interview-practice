import os
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# name, window_ms, max_weight, capacity, refill_per_sec
TIERS = [
    ("free", 10000, 8, 3, 1),
    ("basic", 10000, 30, 10, 3),
    ("pro", 30000, 200, 50, 20),
    ("bulk", 20000, 100000, 200, 20),
]

EXAMPLE_LIMITS = [
    "* 1000 4 2 2",
    "ada 1000 4 3 1",
    "bob 2000 3 2 4",
]

EXAMPLE_REQUESTS = [
    "0.0 ada 1",
    "0.1 ada 1",
    "0.2 ada 1",
    "0.25 bob 1",
    "0.3 ada 1",
    "0.4 ada 1",
    "0.75 bob 2",
    "1.0 ada 1",
    "1.2 bob 1",
    "1.5 cy 3",
]

_CACHE = {}


def _stamp(millis):
    fraction = f"{millis % 1000:03d}".rstrip("0") or "0"
    return f"{millis // 1000}.{fraction}"


def generate(clients, count, span_ms, tier_weights, seed):
    rng = random.Random(seed)
    names = [f"c{index:05d}" for index in range(clients)]

    limit_lines = ["* 10000 8 3 1"]
    tiers = []
    for name in names:
        tier = rng.choices(TIERS, weights=tier_weights)[0]
        tiers.append(tier)
        limit_lines.append(f"{name} {tier[1]} {tier[2]} {tier[3]} {tier[4]}")

    heavy = max(1, clients // 10)
    pick_weights = [8.0 if index < heavy else 1.0 for index in range(clients)]

    picks = rng.choices(range(clients), weights=pick_weights, k=count)
    times = sorted(rng.randrange(span_ms) for _ in range(count))
    lines = []
    for when, index in zip(times, picks):
        roll = rng.random()
        weight = 1 if roll < 0.75 else (2 if roll < 0.95 else 3)
        lines.append(f"{_stamp(when)} {names[index]} {weight}")
    return limit_lines, lines


def _read(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, encoding="utf-8") as handle:
        return [line.rstrip("\n") for line in handle if line.strip()]


def _cached(key, factory):
    if key not in _CACHE:
        _CACHE[key] = factory()
    return _CACHE[key]


def _generated(key, *args, **kwargs):
    return _cached(key, lambda: generate(*args, **kwargs))


def get_example_limits():
    return list(EXAMPLE_LIMITS)


def get_example_requests():
    return list(EXAMPLE_REQUESTS)


def get_small_limits():
    return _cached("small_limits", lambda: _read("limits_small.txt"))


def get_small_requests():
    return _cached("small_requests", lambda: _read("requests_small.txt"))


def _medium():
    return _generated("medium", 800, 40000, 300000, (4, 4, 2, 0), seed=100002)


def get_medium_limits():
    return _medium()[0]


def get_medium_requests():
    return _medium()[1]


def _large():
    return _generated("large", 3000, 300000, 600000, (4, 4, 2, 0), seed=100003)


def get_large_limits():
    return _large()[0]


def get_large_requests():
    return _large()[1]


def _hot():
    return _generated("hot", 8, 120000, 600000, (0, 0, 0, 1), seed=100004)


def get_hot_limits():
    return _hot()[0]


def get_hot_requests():
    return _hot()[1]
