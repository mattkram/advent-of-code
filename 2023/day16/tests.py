import textwrap
from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT = textwrap.dedent(
    r"""
    .|...\....
    |.-.\.....
    .....|-...
    ........|.
    ..........
    .........\
    ..../.\\..
    .-.-/..|..
    .|....-|.\
    ..//.|....
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 46, id="test-input"),
        pytest.param(REAL_INPUT, 6795, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 51, id="test-input"),
        pytest.param(REAL_INPUT, 7154, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
