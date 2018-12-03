import collections
import itertools


def checksum(data):
    two = 0
    three = 0

    for line in data:
        c = collections.Counter(line)
        if any(v == 2 for v in c.values()):
            two += 1
        if any(v == 3 for v in c.values()):
            three += 1

    return two * three


def common(data):
    for pair in itertools.combinations(data, 2):
        differences = 0
        for c1, c2 in zip(*pair):
            if c1 != c2:
                differences += 1
        if differences == 1:
            return "".join(c1 for c1, c2 in zip(*pair) if c1 == c2)


def test_common():
    data = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""".splitlines()
    assert common(data) == "fgij"


def test_checksum():
    data = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""".splitlines()

    assert checksum(data) == 12


if __name__ == "__main__":
    with open("02_input.txt") as f:
        print(checksum(f))
        f.seek(0)
        print(common(f))
