"""Loaders for the request logs.

Only the small log is committed under ../data. The three bigger logs would be
tens of megabytes of text, so they are rebuilt here from fixed seeds. The same
seed always produces the same lines.

    get_example_lines()  the tiny log used in README.md and main.py
    get_small_lines()    2000 requests over 10 minutes
    get_medium_lines()   15000 requests over 1 hour
    get_large_lines()    200000 requests over 4 hours
    get_wide_lines()     200000 requests over 2 hours

The wide log is not bigger than the large one. It exists because the timed test
that uses it asks for long windows that overlap heavily, which is where a
re-scan per window falls apart.
"""

import os
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

EXAMPLE_LINES = [
    "2026-03-01T00:00:00Z GET /api/users/7 200 40",
    "2026-03-01T00:00:10Z GET /api/users/812 200 60",
    "2026-03-01T00:00:20Z GET /api/search 200 900",
    "2026-03-01T00:00:30Z POST /api/orders/55 201 120",
    "2026-03-01T00:00:45Z GET /health 200 2",
    "2026-03-01T00:01:05Z GET /api/search 200 100",
    "2026-03-01T00:01:20Z GET /api/users/9 200 55",
    "2026-03-01T00:01:40Z POST /api/orders/9001 201 400",
    "2026-03-01T00:01:55Z GET /health 200 3",
    "2026-03-01T00:02:10Z GET /api/search 500 1500",
]

# template, method, typical latency, tail latency
_SHAPES = [
    ("/health", "GET", 2, 8),
    ("/static/app.js", "GET", 6, 30),
    ("/static/style.css", "GET", 5, 25),
    ("/api/sessions", "POST", 35, 210),
    ("/api/users/%d", "GET", 28, 180),
    ("/api/users/%d/profile", "GET", 44, 300),
    ("/api/orders/%d", "GET", 52, 420),
    ("/api/orders/%d/items", "GET", 70, 610),
    ("/api/cart/%d", "PUT", 40, 260),
    ("/api/payments/%d", "POST", 130, 1400),
    ("/api/reports/%d/export", "POST", 260, 2600),
    ("/api/search", "GET", 90, 1100),
]

_CACHE = {}


def _stamps(span):
    out = []
    for offset in range(span):
        day = 1 + offset // 86400
        rest = offset % 86400
        out.append(
            f"2026-03-{day:02d}T{rest // 3600:02d}:{rest % 3600 // 60:02d}:{rest % 60:02d}Z"
        )
    return out


def generate_lines(count, span, seed):
    """Deterministic log lines: `count` requests spread over `span` seconds."""
    rng = random.Random(seed)
    stamps = _stamps(span)
    times = sorted(rng.randrange(span) for _ in range(count))
    lines = []
    for when in times:
        template, method, typical, tail = _SHAPES[rng.randrange(len(_SHAPES))]
        if "%d" in template:
            # A mix of short and long ids, so collapsing them matters.
            ident = rng.randrange(1, 60) if rng.random() < 0.4 else rng.randrange(100, 99999)
            path = template % ident
        else:
            path = template
        roll = rng.random()
        latency = typical + int((tail - typical) * roll * roll * roll)
        status = 500 if rng.random() < 0.01 else (201 if method == "POST" else 200)
        lines.append(f"{stamps[when]} {method} {path} {status} {latency}")
    return lines


def _read(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, encoding="utf-8") as handle:
        return [line.rstrip("\n") for line in handle if line.strip()]


def _cached(key, factory):
    if key not in _CACHE:
        _CACHE[key] = factory()
    return _CACHE[key]


def get_example_lines():
    return list(EXAMPLE_LINES)


def get_small_lines():
    return _cached("small", lambda: _read("log_small.txt"))


def get_medium_lines():
    return _cached("medium", lambda: generate_lines(15000, 3600, seed=90002))


def get_large_lines():
    return _cached("large", lambda: generate_lines(200000, 14400, seed=90003))


def get_wide_lines():
    return _cached("wide", lambda: generate_lines(200000, 7200, seed=90004))
