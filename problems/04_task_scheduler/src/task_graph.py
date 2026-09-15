"""Read this first."""


class TaskGraph:
    """Tasks with durations and prerequisites.

    Vocabulary: when `add_dependency("test", "compile")` is called, "test" depends on
    "compile". "compile" is a dependency of "test", and "test" is a dependent of "compile".
    A task can start only after every one of its dependencies has finished.

    Rules:
      * names are unique; adding a name twice raises ValueError
      * durations are positive integers; anything else raises ValueError
      * dependencies may only be added between tasks that exist (KeyError otherwise)
      * a task may not depend on itself (ValueError)
      * `ready_tasks(done)` lists tasks that are not done and whose dependencies are all done
      * every list this class returns is sorted by name
    """

    def __init__(self):
        self._durations = {}
        self._dependencies = {}
        self._dependents = {}

    def add_task(self, name, duration):
        if name in self._durations:
            raise ValueError(f"task {name!r} already exists")
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError(f"duration must be a positive integer, got {duration!r}")
        self._durations[name] = duration
        self._dependencies[name] = set()
        self._dependents[name] = set()

    def add_dependency(self, task, depends_on):
        """Record that `task` can only start after `depends_on` finishes."""
        if task not in self._durations:
            raise KeyError(task)
        if depends_on not in self._durations:
            raise KeyError(depends_on)
        if task == depends_on:
            raise ValueError(f"task {task!r} cannot depend on itself")
        self._dependencies[task].add(depends_on)
        self._dependents[task].add(depends_on)

    def tasks(self):
        return sorted(self._durations)

    def duration_of(self, name):
        return self._durations[name]

    def dependencies_of(self, name):
        """Tasks that must finish before `name` can start."""
        return sorted(self._dependencies[name])

    def dependents_of(self, name):
        """Tasks that cannot start until `name` has finished."""
        return sorted(self._dependents[name])

    def ready_tasks(self, done):
        """Tasks that are not in `done` and whose dependencies are all in `done`."""
        done = set(done)
        ready = []
        for name, dependencies in self._dependencies.items():
            if dependencies <= done:
                ready.append(name)
        return sorted(ready)

    def total_duration(self):
        return sum(self._durations.values())

    def __len__(self):
        return len(self._durations)

    def __contains__(self, name):
        return name in self._durations
