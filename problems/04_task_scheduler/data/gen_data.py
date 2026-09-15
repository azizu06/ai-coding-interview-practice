"""Generate the task files for the Task Scheduler problem.

Run from this directory: python gen_data.py
Only the small and medium sets are written; see src/task_data.py for the rest.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from task_data import random_dag  # noqa: E402


def write(name, tasks, dependencies):
    path = os.path.join(HERE, name)
    with open(path, "w", encoding="utf-8") as handle:
        for task, duration in tasks:
            handle.write(f"task {task} {duration}\n")
        for task, depends_on in dependencies:
            handle.write(f"dep {task} {depends_on}\n")
    print(f"{name}: {len(tasks)} tasks, {len(dependencies)} dependencies, {os.path.getsize(path)} bytes")


def main():
    write("tasks_small.txt", *random_dag(12, 2, seed=11))
    write("tasks_medium.txt", *random_dag(2000, 3, seed=12))


if __name__ == "__main__":
    main()
