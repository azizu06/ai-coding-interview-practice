import os
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def random_dag(count, max_deps, seed):
    rng = random.Random(seed)
    width = len(str(count))
    names = [f"t{i:0{width}d}" for i in range(1, count + 1)]
    rng.shuffle(names)
    tasks = [(name, rng.randint(1, 20)) for name in names]
    dependencies = []
    for index in range(1, count):
        for _ in range(rng.randint(0, max_deps)):
            earlier = rng.randrange(index)
            dependencies.append((names[index], names[earlier]))
    return tasks, sorted(set(dependencies))


def chain(count, seed):
    rng = random.Random(seed)
    width = len(str(count))
    names = [f"c{i:0{width}d}" for i in range(1, count + 1)]
    rng.shuffle(names)
    tasks = [(name, rng.randint(1, 5)) for name in names]
    dependencies = [(names[i], names[i - 1]) for i in range(1, count)]
    return tasks, dependencies


def _read(name):
    tasks = []
    dependencies = []
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as handle:
        for line in handle:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "task":
                tasks.append((parts[1], int(parts[2])))
            elif parts[0] == "dep":
                dependencies.append((parts[1], parts[2]))
    return tasks, dependencies


def get_example_tasks():
    tasks = [("fetch", 2), ("compile", 5), ("lint", 1), ("test", 4), ("package", 2), ("deploy", 3)]
    dependencies = [
        ("compile", "fetch"),
        ("lint", "fetch"),
        ("test", "compile"),
        ("package", "compile"),
        ("package", "lint"),
        ("deploy", "test"),
        ("deploy", "package"),
    ]
    return tasks, dependencies


def get_small_tasks():
    return _read("tasks_small.txt")


def get_medium_tasks():
    return _read("tasks_medium.txt")


def get_large_tasks():
    return random_dag(20000, 3, seed=20260904)


def get_huge_tasks():
    return random_dag(100000, 3, seed=20260905)


def get_long_tasks():
    return chain(50000, seed=20260906)
