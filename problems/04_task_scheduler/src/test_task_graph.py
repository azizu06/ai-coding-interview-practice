import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_graph import TaskGraph  # noqa: E402


def pipeline():
    graph = TaskGraph()
    for name, duration in [("fetch", 2), ("compile", 5), ("lint", 1), ("test", 4), ("package", 2), ("deploy", 3)]:
        graph.add_task(name, duration)
    for task, depends_on in [("compile", "fetch"), ("lint", "fetch"), ("test", "compile"),
                             ("package", "compile"), ("package", "lint"), ("deploy", "test"), ("deploy", "package")]:
        graph.add_dependency(task, depends_on)
    return graph


class TestAddTask(unittest.TestCase):
    def test_add_and_read_back(self):
        graph = TaskGraph()
        graph.add_task("fetch", 2)
        self.assertEqual(graph.tasks(), ["fetch"])
        self.assertEqual(graph.duration_of("fetch"), 2)
        self.assertIn("fetch", graph)
        self.assertEqual(len(graph), 1)

    def test_duplicate_name_is_rejected(self):
        graph = TaskGraph()
        graph.add_task("fetch", 2)
        with self.assertRaises(ValueError):
            graph.add_task("fetch", 3)

    def test_bad_duration_is_rejected(self):
        graph = TaskGraph()
        with self.assertRaises(ValueError):
            graph.add_task("fetch", 0)
        with self.assertRaises(ValueError):
            graph.add_task("fetch", 2.5)

    def test_tasks_are_sorted(self):
        graph = pipeline()
        self.assertEqual(graph.tasks(), ["compile", "deploy", "fetch", "lint", "package", "test"])
        self.assertEqual(graph.total_duration(), 17)


class TestDependencies(unittest.TestCase):
    def test_dependencies_of(self):
        graph = pipeline()
        self.assertEqual(graph.dependencies_of("package"), ["compile", "lint"])
        self.assertEqual(graph.dependencies_of("fetch"), [])

    def test_unknown_task_is_rejected(self):
        graph = pipeline()
        with self.assertRaises(KeyError):
            graph.add_dependency("fetch", "ghost")
        with self.assertRaises(KeyError):
            graph.add_dependency("ghost", "fetch")

    def test_self_dependency_is_rejected(self):
        graph = pipeline()
        with self.assertRaises(ValueError):
            graph.add_dependency("fetch", "fetch")

    def test_ready_at_start(self):
        graph = pipeline()
        self.assertEqual(graph.ready_tasks(set()), ["fetch"])

    # def test_dependents_of(self):
    #     graph = pipeline()
    #     expected = "????"
    #     self.assertEqual(graph.dependents_of("fetch"), expected)

    # def test_dependents_of_final_task(self):
    #     graph = pipeline()
    #     expected = "????"
    #     self.assertEqual(graph.dependents_of("deploy"), expected)

    # def test_ready_after_fetch(self):
    #     graph = pipeline()
    #     expected = "????"
    #     self.assertEqual(graph.ready_tasks({"fetch"}), expected)

    # def test_ready_when_everything_is_done(self):
    #     graph = pipeline()
    #     expected = "????"
    #     self.assertEqual(graph.ready_tasks(set(graph.tasks())), expected)


if __name__ == "__main__":
    unittest.main()
