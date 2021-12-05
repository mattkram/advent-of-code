from pathlib import Path

import pytest

from .solution import calculate

TEST_INPUT = """
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2
"""

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 5),
        (REAL_INPUT, 5167),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str, consider_diagonals=False) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 12),
        (REAL_INPUT, 17604),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, consider_diagonals=True) == expected
