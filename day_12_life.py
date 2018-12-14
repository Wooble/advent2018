"""1-D Game of life, essentially."""


EXAMPLE_INPUT = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""


def parse_input(input_data):
    lines = input_data.splitlines()
    state_string = lines[0].split(": ")[1].strip()
    state = {idx: True for idx, c in enumerate(state_string) if c == "#"}
    rules = set()
    for line in lines[2:]:
        if "=> #" in line:
            rules.add(tuple(c == "#" for c in line[:5]))
    return state, rules


def test_checksum():
    assert checksum(EXAMPLE_INPUT) == 325


def state_after(data, iterations):
    state, rules = parse_input(data)

    for _ in range(iterations):
        state = apply_rules(state, rules)

    return state


def checksum(data):
    state = state_after(data, 20)

    return sum(k for k, v in state.items() if v)


def apply_rules(state, rules):
    newstate = {}

    for cell in range(min(state.keys()) - 4, max(state.keys()) + 4):
        rule = tuple(state.get(slot, False) for slot in range(cell - 2, cell + 3))
        if rule in rules:
            newstate[cell] = True

    return newstate


def calculated_checksum(data, iterations):
    state = state_after(data, 500)
    # assumption: stable pattern moves right one space per iteration after this, based on observation in debugger

    return sum(k + iterations - 500 for k in state.keys())


if __name__ == "__main__":
    with open("12_input.txt") as f:
        real_input = f.read()

    print(checksum(real_input))
    print(calculated_checksum(real_input, 50_000_000_000))
