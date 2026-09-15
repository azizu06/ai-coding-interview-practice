"""Brute force reference: rescan every task each round, then relax finish times until stable.

`ready_tasks` scans every task, so building the order costs O(V * (V + E)). The finish
times repeat a full pass over the graph until nothing changes, which is O(depth * (V + E))
and turns quadratic on a long chain.
"""

from task_graph import TaskGraph


class Solver:
    def __init__(self, graph: TaskGraph):
        self.graph = graph

    def execution_order(self):
        graph = self.graph
        done = set()
        order = []
        while len(order) < len(graph):
            ready = graph.ready_tasks(done)
            if not ready:
                raise ValueError("the task graph has a cycle")
            name = ready[0]
            done.add(name)
            order.append(name)
        return order

    def finish_times(self):
        graph = self.graph
        if self.has_cycle():
            raise ValueError("the task graph has a cycle")
        finish = {name: graph.duration_of(name) for name in graph.tasks()}
        changed = True
        while changed:
            changed = False
            for name in graph.tasks():
                start = max((finish[dependency] for dependency in graph.dependencies_of(name)), default=0)
                candidate = start + graph.duration_of(name)
                if candidate > finish[name]:
                    finish[name] = candidate
                    changed = True
        return finish

    def has_cycle(self):
        try:
            self.execution_order()
        except ValueError:
            return True
        return False
