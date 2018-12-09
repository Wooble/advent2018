import collections
import pytest


@pytest.fixture
def exampledata():
    return collections.deque(
        int(x) for x in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split()
    )


def test_metadata_sum(exampledata):
    assert metadata_sum(exampledata) == 138


def test_rootval(exampledata):
    assert rootval(exampledata) == 66


def metadata_sum(data):
    num_children = data.popleft()
    num_metadata = data.popleft()
    mdsum = 0
    for _ in range(num_children):
        mdsum += metadata_sum(data)
    for _ in range(num_metadata):
        mdsum += data.popleft()
    return mdsum


def rootval(data):
    num_children = data.popleft()
    num_metadata = data.popleft()
    children = []
    metadata = []

    for _ in range(num_children):
        children.append(rootval(data))
    for _ in range(num_metadata):
        metadata.append(data.popleft())

    if not children:
        return sum(metadata)
    else:
        rv = 0
        for x in metadata:
            if x:
                try:
                    rv += children[x - 1]
                except IndexError:
                    pass
        return rv


if __name__ == "__main__":
    with open("08_input.txt") as f:
        data = [int(x) for x in f.read().split()]
    print(metadata_sum(collections.deque(data)))
    print(rootval(collections.deque(data)))
