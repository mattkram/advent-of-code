from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT = """
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
"""


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected,num_steps",
    [
        (TEST_INPUT, 204, 10),
        (TEST_INPUT, 1656, 100),
        (REAL_INPUT, 1743, 100),
    ],
)
def test_part1(input_str: str, expected: int, num_steps: int) -> None:
    assert calculate_part1(input_str, num_steps) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 195),
        (REAL_INPUT, 364),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
