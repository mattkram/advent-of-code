from pathlib import Path

import pytest

from .solution import calculate

TEST_INPUT = """
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
"""


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 1588),
        (REAL_INPUT, 3118),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 10),
        # (REAL_INPUT, 50),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, num_steps=40) == expected
