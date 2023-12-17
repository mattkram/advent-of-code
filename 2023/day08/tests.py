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
        pytest.param(TEST_INPUT, 5905, id="test-input"),
        pytest.param(REAL_INPUT, 244848487, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, part=2) == expected
