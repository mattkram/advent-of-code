import textwrap
from pathlib import Path

import pytest

from .solution import calculate


TEST_INPUT = textwrap.dedent(
    """\
    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)
    """
)
TEST_INPUT_2 = textwrap.dedent(
    """\
    LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 2, id="test-input"),
        pytest.param(REAL_INPUT, 17141, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT_2, 6, id="test-input"),
        pytest.param(REAL_INPUT, 10818234074807, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, part=2) == expected
