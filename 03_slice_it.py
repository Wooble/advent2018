import collections
import itertools
import re


def overlap(data):
    placement = collections.Counter()
    for line in data:
        numbers = re.search(r"@ (\d+),(\d+): (\d+)x(\d+)", line)
        x, y, w, h = (int(i) for i in numbers.group(1, 2, 3, 4))
        for x1, y1 in itertools.product(range(x, x + w), range(y, y + h)):
            placement[(x1, y1)] += 1
    return sum(1 for count in placement.values() if count > 1)


def no_overlap(data):
    claims = []
    placement = collections.defaultdict(list)
    overlaps = set()
    for line in data:
        numbers = re.search(r"(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
        claim, x, y, w, h = (int(i) for i in numbers.group(1, 2, 3, 4, 5))
        claims.append(claim)
        for x1, y1 in itertools.product(range(x, x + w), range(y, y + h)):
            placement[(x1, y1)].append(claim)
            if len(placement[(x1, y1)]) > 1:
                overlaps.update(placement[(x1, y1)])
    return (set(claims) - overlaps).pop()


def test_overlap():
    data = ["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]
    assert overlap(data) == 4


def test_no_overlap():
    data = ["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]
    assert no_overlap(data) == 3


if __name__ == "__main__":
    with open("03_input.txt") as infile:
        print(overlap(infile))
        infile.seek(0)
        print(no_overlap(infile))
