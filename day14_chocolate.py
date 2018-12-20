import pytest


def ten_scores(after):
    elves = [0, 1]
    board = [3, 7]
    while len(board) < after + 10:
        new_recipies = sum(board[elves[x]] for x in (0,1))
        for digit in str(new_recipies):
            board.append(int(digit))
        for idx, elf in enumerate(elves):
            elves[idx] = (elf + 1 + board[elf]) % len(board)
        #print(board, elves)
    return ''.join(str(digit) for digit in board[after:after+10])


@pytest.mark.parametrize("after,expected",
                         [
                             (9, "5158916779"),
                             (5, "0124515891"),
                             (18, "9251071085"),
                             (2018, "5941429882"),
                         ])
def test_ten_scores(after, expected):
    assert ten_scores(after) == expected


@pytest.mark.parametrize("searchscore,expected", [
    ("51589", 9),
    ("01245", 5),
    ("92510", 18),
    ("59414", 2018),
    ("515891", 9)
])
def test_search(searchscore,expected):
    assert search(searchscore) == expected


def search(searchscore):
    # refactorme
    elves = [0, 1]
    board = [3, 7]
    search = [int(x) for x in searchscore]
    while (board[-len(search):] != search) and (board[-(len(search)+1):-1] != search):
        new_recipies = sum(board[elves[x]] for x in (0,1))
        for digit in str(new_recipies):
            board.append(int(digit))
        for idx, elf in enumerate(elves):
            elves[idx] = (elf + 1 + board[elf]) % len(board)
    if board[-len(search):] == search:
        return len(board) - len(search)
    else:
        return len(board) - len(search) - 1


if __name__ == "__main__":
    print(ten_scores(909441))
    print(search("909441"))
