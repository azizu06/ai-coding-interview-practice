"""Reference solution: Kahn's algorithm with a heap, then one pass for finish times.

Every task starts with a count of unfinished dependencies. Tasks whose count is zero sit
in a min-heap so the alphabetically smallest ready task always comes out first. Popping a
task decrements the count of each dependent and pushes it when it reaches zero. That is
O((V + E) log V). If the order is shorter than the task count, something never reached
zero, which means a cycle.

Finish times fall out of one walk over that order: a task's dependencies all appear
earlier in the order, so their finish times are already known. O(V + E), no recursion.
"""

import heapq

from task_graph import TaskGraph


class Solver:
    def __init__(self, graph: TaskGraph):
        self.graph = graph

    def _topological_order(self):
        graph = self.graph
        pending = {}
        dependents = {}
        heap = []
        for name in graph.tasks():
            count = len(graph.dependencies_of(name))
            pending[name] = count
            dependents[name] = graph.dependents_of(name)
            if count == 0:
                heap.append(name)
        heapq.heapify(heap)
        order = []
        while heap:
            name = heapq.heappop(heap)
            order.append(name)
            for dependent in dependents[name]:
                pending[dependent] -= 1
                if pending[dependent] == 0:
                    heapq.heappush(heap, dependent)
        return order

    def execution_order(self):
        order = self._topological_order()
        if len(order) != len(self.graph):
            raise ValueError("the task graph has a cycle")
        return order

    def finish_times(self):
        graph = self.graph
        finish = {}
        for name in self.execution_order():
            start = max((finish[dependency] for dependency in graph.dependencies_of(name)), default=0)
            finish[name] = start + graph.duration_of(name)
        return finish

    def has_cycle(self):
        return len(self._topological_order()) != len(self.graph)
