from pathlib import Path

import pytest

from .solution import calculate

TEST_INPUT = """
    Time:      7  15   30
    Distance:  9  40  200
"""

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 288, id="test-input"),
        pytest.param(REAL_INPUT, 3316275, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 71503, id="test-input"),
        pytest.param(REAL_INPUT, 27102791, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, concat=True) == expected
