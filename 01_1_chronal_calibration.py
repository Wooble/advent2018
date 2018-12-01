import re
import pytest


def frequency(changes: str) -> int:
    """Calculate final frequency from changes."""
    current_freq = 0
    changes_list = re.split(r"[,\n]", changes, flags=re.MULTILINE)
    for change in (int(x) for x in changes_list if x):
        current_freq += change
    return current_freq


@pytest.mark.parametrize('freq_changes,expected', [
    ("+1, +1, +1", 3),
    ("+1, +1, -2", 0),
    ("-1, -2, -3", -6),
    ("+1\n+1\n+1", 3),  # actual input is \n separated
])
def test_frequency(freq_changes: str, expected: int):
    assert frequency(freq_changes) == expected


if __name__ == "__main__":
    with open('01_1_input.txt') as f:
        print(frequency(f.read()))
