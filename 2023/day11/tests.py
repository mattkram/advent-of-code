import textwrap
from pathlib import Path

import pytest

from .solution import calculate_part1, calculate_part2

TEST_INPUT = textwrap.dedent(
    """\
    ...#......
    .......#..
    #.........
    ..........
    ......#...
    .#........
    .........#
    ..........
    .......#..
    #...#.....
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 374, id="test-input"),
        pytest.param(REAL_INPUT, 9214785, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expansion_factor,expected",
    [
        pytest.param(TEST_INPUT, 10, 1030, id="test-input"),
        pytest.param(TEST_INPUT, 100, 8410, id="test-input"),
        pytest.param(REAL_INPUT, 1_000_000, 613686987427, id="real-data"),
    ],
)
def test_part2(input_str: str, expansion_factor, expected: int) -> None:
    assert calculate_part2(input_str, expansion_factor=expansion_factor) == expected
