def test_straight():
    INPUT = """|
v
|
|
|
^
|
"""
    assert collision_loc(INPUT) == (0, 3)

def test_example_two():
    INPUT = """/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
  """
    assert collision_loc(INPUT) == (7, 3)


def collision_loc(data):
    pass
