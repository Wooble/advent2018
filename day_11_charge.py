import numpy as np
import pytest


@pytest.mark.parametrize(
    "loc,serial,expected",
    [((3, 5), 8, 4), ((122, 79), 57, -5), ((217, 196), 39, 0), ((101, 153), 71, 4)],
)
def test_power_level(loc, serial, expected):
    assert power_level(loc, serial) == expected


@pytest.mark.parametrize("serial,expected", [(18, (33, 45)), (42, (21, 61))])
def test_biggest_total(serial, expected):
    assert biggest_total(serial) == expected


@pytest.mark.parametrize("num,expected", [(12345, 3), (5, 0)])
def test_hundreds(num, expected):
    assert hundreds(num) == expected


def hundreds(num: int) -> int:
    """Get hundreds digit from a number"""
    return (num // 100) % 10


def power_level(loc: tuple, serial: int) -> int:
    """Calculate power level of a single cell."""
    x, y = loc
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = hundreds(power)
    return power - 5


def make_grid(serial):
    grid = np.zeros((301, 301))
    for (x, y), _ in np.ndenumerate(grid):
        if x * y:
            grid[x][y] = power_level((x, y), serial)
    return grid


def biggest_total_and_total(serial, size):
    grid = make_grid(serial)

    def keyfunc(item):
        x, y = item[0]
        if x + size > 300 or y + size > 300:
            return float("-Inf")
        return np.sum(grid[x : x + size, y : y + size])

    element = max(np.ndenumerate(grid), key=keyfunc)
    return element[0], keyfunc(element)


def biggest_total(serial: int, size: int = 3) -> tuple:
    """Find the coordinates of the upper left corner of the highest power 3x3 region."""
    return biggest_total_and_total(serial, size)[0]


def biggest_total_anysize(serial):
    solutions = []
    for size in range(1, 301):
        solutions.append((biggest_total_and_total(serial, size), size))
    solution = max(solutions, key=lambda item: item[0][1])
    return solution


if __name__ == "__main__":
    print(biggest_total(9810))
    print(biggest_total_anysize(9810))
