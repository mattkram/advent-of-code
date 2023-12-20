import textwrap
from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT_1 = textwrap.dedent(
    """\
    .....
    .S-7.
    .|.|.
    .L-J.
    .....
    """
)
TEST_INPUT_2 = textwrap.dedent(
    """\
    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...
    """
)

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT_1, 4, id="test-input"),
        pytest.param(TEST_INPUT_2, 8, id="test-input"),
        pytest.param(REAL_INPUT, 6942, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT_1, 114, id="test-input"),
        # pytest.param(REAL_INPUT, 1921197370, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
