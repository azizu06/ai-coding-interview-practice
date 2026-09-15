"""Runnable demo. Try: python src/main.py"""

from solver import Solver
from task_data import get_example_tasks
from task_graph import TaskGraph


def build_graph(tasks, dependencies):
    graph = TaskGraph()
    for name, duration in tasks:
        graph.add_task(name, duration)
    for task, depends_on in dependencies:
        graph.add_dependency(task, depends_on)
    return graph


def main():
    print("BEGIN task scheduler demo")
    tasks, dependencies = get_example_tasks()
    graph = build_graph(tasks, dependencies)
    print(f"{len(graph)} tasks, total duration {graph.total_duration()}")
    for name in graph.tasks():
        print(f"  {name:8} {graph.duration_of(name):2}  needs {graph.dependencies_of(name)}  unblocks {graph.dependents_of(name)}")
    print(f"ready at start: {graph.ready_tasks(set())}")
    print(f"ready after fetch: {graph.ready_tasks({'fetch'})}")
    solver = Solver(graph)
    print(f"has cycle: {solver.has_cycle()}")
    print(f"execution order: {solver.execution_order()}")
    print(f"finish times: {solver.finish_times()}")
    print("END task scheduler demo")


if __name__ == "__main__":
    main()
