from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT = """
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
"""


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 40),
        (REAL_INPUT, 824),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 10),
        # (REAL_INPUT, 50),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
