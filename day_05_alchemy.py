import itertools
import string

TESTDATA = "dabAcCaCBAcCcaDA"


def one_pass(data):
    pairs = itertools.zip_longest(data, data[1:])
    output = []
    for p1, p2 in pairs:
        if p1.swapcase() == p2:
            next(pairs)
        else:
            output.append(p1)
    return "".join(output)


def alchemy(data):
    old = data
    while True:
        new = one_pass(old)
        if len(new) == len(old):
            return new
        old = new


def drop_letter(c, data):
    return data.replace(c, "").replace(c.upper(), "")


def best_removed(data):
    return min(
        len(a) for a in (alchemy(drop_letter(c, data)) for c in string.ascii_lowercase)
    )


def test_alchemy():
    assert len(alchemy(TESTDATA)) == 10


def test_best_removed():
    assert best_removed(TESTDATA) == 4


if __name__ == "__main__":
    with open("05_input.txt") as f:
        real_data = f.read().strip()

    print(len(alchemy(real_data)))
    print(best_removed(real_data))
