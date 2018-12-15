import collections
from dataclasses import dataclass

CART_DIRS = {
    "^": ((0, -1), "|"),
    "v": ((0, 1,), "|"),
    "<": ((-1, 0), "-"),
    ">": ((1, 0), "-"),
}

NEXT_TURN = {
    "L": "S",
    "S": "R",
    "R": "L",
}

def test_straight():
    testdata = """|
v
|
|
|
^
|
"""
    assert collision_loc(testdata) == (0, 3)


def test_example_two():
    testdata = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
  """
    assert collision_loc(testdata) == (7, 3)


def test_last_cart():
    testdata = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
  """
    assert last_cart_loc(testdata) == (6, 4)


@dataclass
class Cart:
    location: tuple
    direction: tuple
    next_turn: str = "L"
    exists: bool = True

    def process_move(self, tracks):
        if not self.exists:
            return
        self.location = (self.location[0] + self.direction[0], self.location[1] + self.direction[1])
        self.change_direction(tracks[self.location])

    def change_direction(self, symbol):
        if symbol == "+":
            if self.next_turn == "L":
                self.turn_left()
            elif self.next_turn == "R":
                self.turn_right()
            self.next_turn = NEXT_TURN[self.next_turn]
        elif symbol == "/":
            if self.direction[0] == 0:
                self.turn_right()
            else:
                self.turn_left()
        elif symbol == "\\":
            if self.direction[0] == 0:
                self.turn_left()
            else:
                self.turn_right()

    def turn_left(self):
        x, y = self.direction
        self.direction = (y, -x)

    def turn_right(self):
        x, y = self.direction
        self.direction = (-y, x)


def parse_data(data):
    tracks = {}
    carts = []

    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char in CART_DIRS:
                carts.append(Cart(location=(x, y), direction=CART_DIRS[char][0]))
                char = CART_DIRS[char][1]
            if char.strip():
                tracks[(x, y)] = char
    return tracks, carts


def collision_loc(data):
    tracks, carts = parse_data(data)

    while True:
        for cart in sorted(carts, key=lambda c: (c.location[1], c.location[0])):
            cart.process_move(tracks)

            loc_count = collections.Counter(cart.location for cart in carts)
            maxloc = loc_count.most_common(1)[0]
            if maxloc[1] > 1:
                return maxloc[0]


def last_cart_loc(data):
    tracks, carts = parse_data(data)

    while True:
        for cart in sorted(carts, key=lambda c: (c.location[1], c.location[0])):
            cart.process_move(tracks)

            loc_count = collections.Counter(cart.location for cart in carts if cart.exists)
            maxloc = loc_count.most_common(1)[0]
            if maxloc[1] > 1:
                for c in carts:
                    if c.location == maxloc[0]:
                        c.exists = False
        carts = [c for c in carts if c.exists]
        if len(carts) == 1:
            return carts[0].location
        if not carts:
            raise ValueError("Out of carts")




if __name__ == "__main__":
    with open("13_input.txt") as f:
        data = f.read()
    print(collision_loc(data))
    print(last_cart_loc(data))
