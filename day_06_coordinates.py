import collections
import itertools


def manhattan(p1, p2):
    return sum(abs(x - y) for x, y in zip(p1, p2))


def nearest_to(point, data):
    data_with_dist = ((i, pt, manhattan(point, pt)) for i, pt in enumerate(data))
    distances = sorted(data_with_dist, key=lambda pt: pt[2])

    if distances[0][2] == distances[1][2]:
        return None
    return distances[0][0]


def largest_area(data, bound):
    possibles = set(range(len(data)))
    mapping = {}
    for pt in itertools.product(range(bound), repeat=2):
        mapping[pt] = nearest_to(pt, data)

    for pt in ((0, y) for y in range(bound)):
        possibles.discard(mapping[pt])
    for pt in ((bound - 1, y) for y in range(bound)):
        possibles.discard(mapping[pt])
    for pt in ((x, 0) for x in range(bound)):
        possibles.discard(mapping[pt])
    for pt in ((x, bound -1) for x in range(bound)):
        possibles.discard(mapping[pt])

    c = collections.Counter(v for v in mapping.values() if v in possibles)
    return c.most_common(1)[0][1]


def total_dist(point, data):
    return sum(manhattan(point, p) for p in data)


def safe_region(data, dist, bound):
    mapping = {}
    for pt in itertools.product(range(bound), repeat=2):
        mapping[pt] = total_dist(pt, data) < dist
    return sum(1 for v in mapping.values() if v)


def test_largest_data():
    example = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
    assert largest_area(example, 20) == 17


def test_safe_region():
    example = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
    assert safe_region(example, 32, 20) == 16


if __name__ == "__main__":
    with open("06_input.txt") as f:
        coordinates = [
            pair for pair in (tuple(int(x) for x in line.split(",")) for line in f)
        ]
        print(largest_area(coordinates, 500))
        print(safe_region(coordinates, 10000, 500))
