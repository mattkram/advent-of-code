from pathlib import Path

import pytest

from .solution import calculate_part1, calculate_part2

TEST_INPUTS_FILE = Path(__file__).parent / "test_input.txt"
with TEST_INPUTS_FILE.open("r") as fp:
    TEST_INPUT = fp.read()


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 79),
        # (REAL_INPUT, 491),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 3621),
        # (REAL_INPUT, 50),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
