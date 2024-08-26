import math
from pathlib import Path
from typing import Tuple

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

TEST_INPUT = """
..##.........##.........##.........##.........##.........##.......
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#
"""

TEST_INPUTS = [
    ((1, 1), 2),
    ((3, 1), 7),
    ((5, 1), 3),
    ((7, 1), 4),
    ((1, 2), 2),
]
SLOPES = [t[0] for t in TEST_INPUTS]


def calculate(input_str: str, slope: Tuple[int, int]) -> int:
    lines = [s.strip() for s in input_str.split("\n") if s.strip()]  # noqa: F841

    right, down = slope

    row, col = 0, 0

    num_trees = 0
    while True:
        row += down
        col += right
        try:
            line = lines[row]
        except IndexError:
            break

        num_trees += int(line[col % len(line)] == "#")

    return num_trees


@pytest.mark.parametrize("input_slope,expected", TEST_INPUTS)
def test(input_slope: Tuple[int, int], expected: int) -> None:
    assert calculate(TEST_INPUT, input_slope) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        return math.prod(calculate(input_str, slope) for slope in SLOPES)


if __name__ == "__main__":
    print(f"The answer is {main()}")
