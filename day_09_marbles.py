import collections

import pytest


@pytest.fixture(params=[
    ("9 players; last marble is worth 25 points", 32),
    ("10 players; last marble is worth 1618 points", 8317),
    ("13 players; last marble is worth 7999 points", 146373),
    ("17 players; last marble is worth 1104 points", 2764),
    ("21 players; last marble is worth 6111 points", 54718),
    ("30 players; last marble is worth 5807 points", 37305),
])
def exampledata(request):
    return request.param


def test_highscore(exampledata):
    assert highscore(exampledata[0]) == exampledata[1]


def parse_data(data):
    parts = data.split()
    return int(parts[0]), int(parts[-2])


def highscore(data):
    num_players, last_marble = parse_data(data)

    scores = calc_scores(last_marble, num_players)
    return max(scores)


def highscore_big(data):
    num_players, last_marble = parse_data(data)
    last_marble *= 100

    scores = calc_scores(last_marble, num_players)
    return max(scores)


def calc_scores(last_marble, num_players):
    board = collections.deque([0])
    scores = [0] * num_players
    current_player = 0
    for current_marble in range(1, last_marble + 1):
        if current_marble % 23:
            board.rotate(-1)
            board.append(current_marble)
        else:
            scores[current_player] += current_marble
            board.rotate(7)
            scores[current_player] += board.pop()
            board.rotate(-1)
        current_player += 1
        current_player %= num_players
    return scores


if __name__ == "__main__":
    with open("09_input.txt") as f:
        data = f.readline().strip()
    print(highscore(data))
    print(highscore_big(data))