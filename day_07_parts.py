import collections
import pytest
import itertools


@pytest.fixture
def data():
    lines = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".splitlines()
    return lines


def test_step_order(data):
    assert step_order(data) == "CABDFE"


def step_order(lines):
    final_order = []
    deps = get_deps(lines)

    while deps:
        doing = sorted(dep for dep in deps.items() if not len(dep[1]))[0][0]
        final_order.append(doing)
        for step in deps.values():
            step.discard(doing)
        del deps[doing]
    return "".join(final_order)


def get_deps(lines):
    deps = collections.defaultdict(set)
    for line in lines:
        parts = line.partition(" must be finished before step ")
        before = parts[0][-1]
        then = parts[2][0]
        deps[then].add(before)
        deps[before]  # Create an empty set to cover the first item with no deps
    return deps


def test_time(data):
    assert (time(data, 2, 0)) == 15


def time_for_task(t: str, delay: int) -> int:
    return ord(t) - ord("A") + 1 + delay


def time(data, workers: int, delay: int):
    deps = get_deps(data)
    worker_pool = [None] * workers
    for current_time in itertools.count():
        # work on existing tasks
        for i, worker in enumerate(worker_pool):
            if worker is not None:
                worker[1] -= 1
                if not worker[1]:
                    # Worker is finished;
                    for step in deps.values():
                        step.discard(worker[0])
                    worker_pool[i] = None

        # queue up some more tasks
        available_tasks = sorted(dep for dep in deps.items() if not len(dep[1]))
        if not deps and all(w is None for w in worker_pool):
            return current_time
        for task in available_tasks:
            for i, worker in enumerate(worker_pool):
                if worker is None:
                    worker_pool[i] = [task[0], time_for_task(task[0], delay)]
                    del deps[task[0]]
                    break


if __name__ == "__main__":
    test_time(data())
    with open("07_input.txt") as f:
        lines = f.readlines()
    print(step_order(lines))
    print(time(lines, 5, 60))
