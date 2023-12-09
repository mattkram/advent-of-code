from pathlib import Path

import pytest

from .solution import calculate

TEST_INPUT = """
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
"""

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 35),
        (REAL_INPUT, 261668924),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 12),
        (REAL_INPUT, 17604),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, diagonals=True) == expected
