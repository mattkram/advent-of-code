import itertools
from pathlib import Path
from typing import Dict, Tuple

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

Coordinate = Tuple[int, int, int, int]


class Board:
    def __init__(self) -> None:
        self._cells: Dict[Coordinate, bool] = {}

    def __getitem__(self, index: Coordinate) -> bool:
        return self._cells.get(index, False)

    def __setitem__(self, index: Coordinate, value: bool) -> None:
        self._cells[index] = value

    def get_num_active_neighbors(self, coords: Coordinate) -> int:
        num_neighbors = 0
        for deltas in itertools.product([-1, 0, 1], repeat=len(coords)):
            if all(d == 0 for d in deltas):
                continue
            new_coords = [c + d for c, d in zip(coords, deltas)]
            neighbor_state = self[tuple(new_coords)]  # type: ignore
            num_neighbors += int(neighbor_state)
        return num_neighbors

    @property
    def min_dim(self) -> Coordinate:
        min_dim = (0, 0, 0, 0)
        for coords in self._cells:
            min_dim = tuple(min(min_dim[i], coords[i]) for i in range(4))  # type: ignore
        return min_dim

    @property
    def max_dim(self) -> Coordinate:
        max_dim = (0, 0, 0, 0)
        for coords in self._cells:
            max_dim = tuple(max(max_dim[i], coords[i]) for i in range(4))  # type: ignore
        return max_dim

    @property
    def num_active(self) -> int:
        return sum(int(v) for v in self._cells.values())


def parse(input_str: str) -> Board:
    board = Board()
    for y, line in enumerate(input_str.strip().splitlines()):
        for x, state in enumerate(line.strip()):
            if state == "#":
                board[x, y, 0, 0] = True
    return board


def calculate(board: Board) -> int:
    for i in range(6):
        ranges = [
            range(min_ - 1, max_ + 2)
            for min_, max_ in zip(board.min_dim, board.max_dim)
        ]
        changes = {}
        for coords in itertools.product(*ranges):
            num_active = board.get_num_active_neighbors(coords)  # type: ignore
            if board[coords]:  # type: ignore
                if num_active != 2 and num_active != 3:
                    changes[coords] = False
            else:
                if num_active == 3:
                    changes[coords] = True

        for coords, value in changes.items():
            board[coords] = value  # type: ignore

    return board.num_active


TEST_INPUTS = [
    (
        """
        .#.
        ..#
        ###
        """,
        848,
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
