import itertools
from pathlib import Path
from typing import Dict, Tuple

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

Coordinate = Tuple[int, int, int]


class Board:
    def __init__(self) -> None:
        self._cells: Dict[Coordinate, bool] = {}

    def __getitem__(self, index: Coordinate) -> bool:
        return self._cells.get(index, False)

    def __setitem__(self, index: Coordinate, value: bool) -> None:
        self._cells[index] = value

    def get_num_active_neighbors(self, coords: Coordinate) -> int:
        (x, y, z) = coords
        num_neighbors = 0
        for dx, dy, dz in itertools.product([-1, 0, 1], repeat=3):
            if (dx, dy, dz) == (0, 0, 0):
                continue
            neighbor_state = self[x + dx, y + dy, z + dz]
            num_neighbors += int(neighbor_state)
        return num_neighbors

    @property
    def min_dim(self) -> Coordinate:
        min_dim = (0, 0, 0)
        for coords in self._cells:
            min_dim = tuple(min(min_dim[i], coords[i]) for i in range(3))  # type: ignore
        return min_dim

    @property
    def max_dim(self) -> Coordinate:
        max_dim = (0, 0, 0)
        for coords in self._cells:
            max_dim = tuple(max(max_dim[i], coords[i]) for i in range(3))  # type: ignore
        return max_dim

    @property
    def num_active(self) -> int:
        return sum(int(v) for v in self._cells.values())


def parse(input_str: str) -> Board:
    board = Board()
    for y, line in enumerate(input_str.strip().splitlines()):
        for x, state in enumerate(line.strip()):
            if state == "#":
                board[x, y, 0] = True
    return board


def calculate(board: Board) -> int:
    for i in range(6):
        min_x, min_y, min_z = board.min_dim
        max_x, max_y, max_z = board.max_dim
        changes = {}
        for coords in itertools.product(
            range(min_x - 1, max_x + 2),
            range(min_y - 1, max_y + 2),
            range(min_z - 1, max_z + 2),
        ):
            num_active = board.get_num_active_neighbors(coords)
            if board[coords]:  # is active
                if num_active != 2 and num_active != 3:
                    changes[coords] = False
            else:
                if num_active == 3:
                    changes[coords] = True

        for coords, value in changes.items():
            board[coords] = value

    return board.num_active


TEST_INPUTS = [
    (
        """
        .#.
        ..#
        ###
        """,
        112,
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
