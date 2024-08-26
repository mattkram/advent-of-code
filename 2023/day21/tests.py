import textwrap
from pathlib import Path

import pytest

from .solution import calculate_part1, calculate_part2

TEST_INPUT = textwrap.dedent(
    """\
    ...........
    .....###.#.
    .###.##..#.
    ..#.#...#..
    ....#.#....
    .##..S####.
    .##..#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str, num_steps, expected",
    [
        pytest.param(TEST_INPUT, 6, 16, id="test-input"),
        pytest.param(REAL_INPUT, 64, 3729, id="real-data"),
    ],
)
def test_part1(input_str: str, num_steps: int, expected: int) -> None:
    assert calculate_part1(input_str, num_steps=num_steps) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 114, id="test-input"),
        # pytest.param(REAL_INPUT, 1921197370, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
