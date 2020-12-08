from pathlib import Path

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"


def calculate(input_str: str) -> int:
    lines = [s.strip() for s in input_str.split("\n") if s.strip()]  # noqa: F841

    right, down = 3, 1

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


TEST_INPUTS = [
    (
        """
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
        .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.
        """,
        7,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(fp.read())


if __name__ == "__main__":
    print(f"The answer is {main()}")
