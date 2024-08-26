from copy import deepcopy
from pathlib import Path
from typing import List

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[List[str]]


FLOOR = "."
EMPTY = "L"
TAKEN = "#"

DIRECTIONS = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)]


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    return [list(line) for line in lines]


def get_num_taken(data: ParsedInput, row: int, col: int) -> int:
    num_taken = 0
    for direction in DIRECTIONS:
        new_row, new_col = row, col
        while True:
            new_row += direction[0]
            new_col += direction[1]

            if new_row < 0 or new_col < 0:
                break

            try:
                neighbor = data[new_row][new_col]
            except IndexError:
                break

            if neighbor == TAKEN:
                num_taken += 1
                break
            elif neighbor == EMPTY:
                break

    return num_taken


def calculate(data: ParsedInput) -> int:
    while True:
        is_changed = False
        new_data = deepcopy(data)
        for i, row in enumerate(data):
            for j, seat in enumerate(row):
                num_taken = get_num_taken(data, i, j)
                if seat == EMPTY and num_taken == 0:
                    new_data[i][j] = TAKEN
                    is_changed = True
                elif seat == TAKEN and num_taken >= 5:
                    new_data[i][j] = EMPTY
                    is_changed = True
        if not is_changed:
            break

        data = new_data
    return sum(sum(seat == TAKEN for seat in row) for row in data)


TEST_INPUTS = [
    (
        """
        L.LL.LL.LL
        LLLLLLL.LL
        L.L.L..L..
        LLLL.LL.LL
        L.LL.LL.LL
        L.LLLLL.LL
        ..L.L.....
        LLLLLLLLLL
        L.LLLLLL.L
        L.LLLLL.LL
        """,
        26,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
