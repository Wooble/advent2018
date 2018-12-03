import itertools
import typing
import pytest


def frequency(changes: typing.Iterable[int]) -> int:
    """Calculate final frequency from changes."""
    seen_freqs = {0}
    current_freq = 0

    for change in itertools.cycle(changes):
        current_freq += change
        if current_freq in seen_freqs:
            return current_freq
        seen_freqs.add(current_freq)


@pytest.mark.parametrize(
    "freq_changes,expected",
    [
        ([+1, -1], 0),
        ([+3, +3, +4, -2, -4], 10),
        ([-6, +3, +8, +5, -6], 5),
        ([+7, +7, -2, -7, -4], 14),
    ],
)
def test_frequency(freq_changes: str, expected: int):
    assert frequency(freq_changes) == expected


if __name__ == "__main__":
    with open("01_1_input.txt") as f:
        print(frequency(int(line) for line in f))
