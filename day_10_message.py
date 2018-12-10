import dataclasses
import re
from typing import Iterable

import pytest

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract"
)


@pytest.fixture
def exampledata():
    return """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".splitlines()


def test_message(exampledata):
    assert message(exampledata) == "HI"


@dataclasses.dataclass
class Light:
    position: tuple
    velocity: tuple


def get_lights(data: Iterable[str]):
    lights = []
    for line in data:
        results = re.match(r"position=<(.*),(.*)> velocity=<(.*),(.*)>", line)
        numbers = [int(x) for x in results.groups()]
        lights.append(Light(position=tuple(numbers[0:2]), velocity=tuple(numbers[2:])))
    return lights


def getsize(lights):
    width = max(light.position[0] for light in lights) - min(
        light.position[0] for light in lights
    )
    length = max(light.position[1] for light in lights) - min(
        light.position[1] for light in lights
    )
    return width + 10, length + 10


def get_adjustment(lights):
    xadj = min(light.position[0] for light in lights) * -1
    yadj = min(light.position[1] for light in lights) * -1
    return xadj + 4, yadj + 4


def adjust(pos, adj):
    return (pos[0] + adj[0], pos[1] + adj[1])


def new_pos(light):
    return light.position[0] + light.velocity[0], light.position[1] + light.velocity[1]


def message(data):
    lights = get_lights(data)
    time = 0
    while True:
        size = getsize(lights)
        adjustment = get_adjustment(lights)
        print(size[0])
        if size[0] < 100:
            im = Image.new("1", size, 1)
            for light in lights:
                location = adjust(light.position, adjustment)
                im.putpixel(location, 0)
            # im.show()

            msg = pytesseract.image_to_string(im)
            if msg:
                return msg, time
        for light in lights:
            light.position = new_pos(light)
        time += 1


if __name__ == "__main__":
    with open("10_input.txt") as f:
        data = f.readlines()
    print(message(data))
