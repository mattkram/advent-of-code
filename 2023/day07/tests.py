import textwrap
from pathlib import Path

import pytest

from .solution import calculate

TEST_INPUT = textwrap.dedent(
    """\
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 6440, id="test-input"),
        pytest.param(REAL_INPUT, 246409899, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 5905, id="test-input"),
        pytest.param(REAL_INPUT, 244848487, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, part=2) == expected
