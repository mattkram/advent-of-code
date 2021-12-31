from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #######
"""


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 12521),
        # (REAL_INPUT, 50),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 44169),
        # (REAL_INPUT, 55136),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
