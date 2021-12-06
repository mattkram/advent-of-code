from pathlib import Path

import pytest

from .solution import calculate

TEST_INPUT = "3,4,3,1,2"

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 5934),
        (REAL_INPUT, 358214),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str, generations=80) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 26984457539),
        (REAL_INPUT, 1622533344325),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, generations=256) == expected
