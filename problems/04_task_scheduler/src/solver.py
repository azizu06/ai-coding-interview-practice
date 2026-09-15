"""You'll implement this."""

from task_graph import TaskGraph


class Solver:
    def __init__(self, graph: TaskGraph):
        self.graph = graph

    def execution_order(self):
        """Return every task name in an order that respects all dependencies.

        When several tasks are ready at the same moment, the one with the alphabetically
        smallest name goes first. Raise ValueError if the graph has a cycle.
        """
        pass

    def finish_times(self):
        """Return {task: earliest finish time} assuming unlimited workers.

        A task starts the moment its last dependency finishes (time 0 when it has none)
        and finishes `duration` later. Raise ValueError if the graph has a cycle.
        """
        pass

    def has_cycle(self):
        """True when some task depends, directly or indirectly, on itself."""
        pass
