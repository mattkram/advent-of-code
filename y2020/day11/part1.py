from copy import deepcopy
from pathlib import Path
from typing import List

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[List[str]]


FLOOR = "."
EMPTY = "L"
TAKEN = "#"


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    return [list(line) for line in lines]


def get_neighbors(data: ParsedInput, row: int, col: int) -> List[str]:
    neighbors = []
    for i in [row - 1, row, row + 1]:
        for j in [col - 1, col, col + 1]:
            if (i, j) == (row, col) or i < 0 or j < 0:
                continue

            try:
                neighbors.append(data[i][j])
            except IndexError:
                pass
    return neighbors


def calculate(data: ParsedInput) -> int:
    while True:
        new_data = deepcopy(data)
        for i, row in enumerate(data):
            for j, seat in enumerate(row):
                neighbors = get_neighbors(data, i, j)
                neighbors_taken = [n for n in neighbors if n == TAKEN]
                if seat == EMPTY and len(neighbors_taken) == 0:
                    new_data[i][j] = TAKEN
                elif seat == TAKEN and len(neighbors_taken) >= 4:
                    new_data[i][j] = EMPTY

        if all(
            old_seat == new_seat
            for old_row, new_row in zip(data, new_data)
            for old_seat, new_seat in zip(old_row, new_row)
        ):
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
        37,
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
