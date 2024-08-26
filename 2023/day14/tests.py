import textwrap
from pathlib import Path

import pytest

from .solution import calculate_part1, calculate_part2

TEST_INPUT = textwrap.dedent(
    """\
    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 136, id="test-input"),
        pytest.param(REAL_INPUT, 108918, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 64, id="test-input"),
        pytest.param(REAL_INPUT, 100310, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
