import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver import Solver  # noqa: E402
from task_data import (  # noqa: E402
    get_example_tasks,
    get_huge_tasks,
    get_large_tasks,
    get_long_tasks,
    get_medium_tasks,
    get_small_tasks,
)
from task_graph import TaskGraph  # noqa: E402


def build_graph(tasks, dependencies):
    graph = TaskGraph()
    for name, duration in tasks:
        graph.add_task(name, duration)
    for task, depends_on in dependencies:
        graph.add_dependency(task, depends_on)
    return graph


def check_order(test, order, tasks, dependencies):
    """Every task exactly once, every dependency before the task that needs it."""
    test.assertEqual(len(order), len(tasks))
    position = {name: index for index, name in enumerate(order)}
    test.assertEqual(len(position), len(tasks))
    for task, depends_on in dependencies:
        test.assertLess(position[depends_on], position[task], f"{depends_on} must run before {task}")


class TestSolverCorrectness(unittest.TestCase):
    def test_example_order_is_valid(self):
        tasks, dependencies = get_example_tasks()
        order = Solver(build_graph(tasks, dependencies)).execution_order()
        check_order(self, order, tasks, dependencies)

    def test_example_has_no_cycle(self):
        self.assertFalse(Solver(build_graph(*get_example_tasks())).has_cycle())

    def test_single_task_finish_time(self):
        graph = build_graph([("solo", 7)], [])
        self.assertEqual(Solver(graph).finish_times(), {"solo": 7})

    def test_independent_tasks_run_alphabetically(self):
        graph = build_graph([("c", 1), ("a", 1), ("b", 1)], [])
        self.assertEqual(Solver(graph).execution_order(), ["a", "b", "c"])

    # def test_example_order(self):
    #     expected = "????"
    #     self.assertEqual(Solver(build_graph(*get_example_tasks())).execution_order(), expected)

    # def test_example_finish_times(self):
    #     expected = "????"
    #     self.assertEqual(Solver(build_graph(*get_example_tasks())).finish_times(), expected)

    # def test_diamond_waits_for_slowest_branch(self):
    #     graph = build_graph([("a", 1), ("b", 5), ("c", 2), ("d", 1)], [("b", "a"), ("c", "a"), ("d", "b"), ("d", "c")])
    #     expected = "????"
    #     self.assertEqual(Solver(graph).finish_times()["d"], expected)

    # def test_cycle_is_detected(self):
    #     graph = build_graph([("a", 1), ("b", 1), ("c", 1), ("d", 1)], [("b", "a"), ("c", "b"), ("a", "c"), ("d", "a")])
    #     solver = Solver(graph)
    #     expected = "????"
    #     self.assertEqual(solver.has_cycle(), expected)
    #     with self.assertRaises(ValueError):
    #         solver.execution_order()
    #     with self.assertRaises(ValueError):
    #         solver.finish_times()

    # def test_small_file(self):
    #     tasks, dependencies = get_small_tasks()
    #     solver = Solver(build_graph(tasks, dependencies))
    #     check_order(self, solver.execution_order(), tasks, dependencies)
    #     expected = "????"
    #     self.assertEqual(max(solver.finish_times().values()), expected)


# Timed tests. Uncomment them for task 6.
# Each one builds the graph up front, starts a clock, computes the order and the finish
# times, and checks the elapsed time plus the makespan (the largest finish time).

class TestSolverSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.medium_tasks, cls.medium_deps = get_medium_tasks()
        cls.large_tasks, cls.large_deps = get_large_tasks()
        cls.huge_tasks, cls.huge_deps = get_huge_tasks()
        cls.long_tasks, cls.long_deps = get_long_tasks()
        cls.medium = build_graph(cls.medium_tasks, cls.medium_deps)
        cls.large = build_graph(cls.large_tasks, cls.large_deps)
        cls.huge = build_graph(cls.huge_tasks, cls.huge_deps)
        cls.long = build_graph(cls.long_tasks, cls.long_deps)

    # def test_medium_2000_tasks(self):
    #     expected_time = 1.0
    #     expected = "????"
    #     start = time.perf_counter()
    #     solver = Solver(self.medium)
    #     order = solver.execution_order()
    #     finish = solver.finish_times()
    #     elapsed = time.perf_counter() - start
    #     check_order(self, order, self.medium_tasks, self.medium_deps)
    #     self.assertEqual(max(finish.values()), expected)
    #     self.assertLess(elapsed, expected_time, f"2000 tasks: {elapsed:.2f}s, need < {expected_time}s")

    # def test_large_20000_tasks(self):
    #     expected_time = 1.0
    #     expected = "????"
    #     start = time.perf_counter()
    #     solver = Solver(self.large)
    #     order = solver.execution_order()
    #     finish = solver.finish_times()
    #     elapsed = time.perf_counter() - start
    #     check_order(self, order, self.large_tasks, self.large_deps)
    #     self.assertEqual(max(finish.values()), expected)
    #     self.assertLess(elapsed, expected_time, f"20000 tasks: {elapsed:.2f}s, need < {expected_time}s")

    # def test_huge_100000_tasks(self):
    #     expected_time = 2.0
    #     expected = "????"
    #     start = time.perf_counter()
    #     solver = Solver(self.huge)
    #     order = solver.execution_order()
    #     finish = solver.finish_times()
    #     elapsed = time.perf_counter() - start
    #     check_order(self, order, self.huge_tasks, self.huge_deps)
    #     self.assertEqual(max(finish.values()), expected)
    #     self.assertLess(elapsed, expected_time, f"100000 tasks: {elapsed:.2f}s, need < {expected_time}s")

    # def test_long_chain_50000_tasks(self):
    #     expected_time = 1.0
    #     expected = "????"
    #     start = time.perf_counter()
    #     solver = Solver(self.long)
    #     order = solver.execution_order()
    #     finish = solver.finish_times()
    #     elapsed = time.perf_counter() - start
    #     check_order(self, order, self.long_tasks, self.long_deps)
    #     self.assertEqual(max(finish.values()), expected)
    #     self.assertLess(elapsed, expected_time, f"50000 chained tasks: {elapsed:.2f}s, need < {expected_time}s")


if __name__ == "__main__":
    unittest.main()
