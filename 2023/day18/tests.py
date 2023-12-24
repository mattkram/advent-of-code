import textwrap
from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT = textwrap.dedent(
    """\
    R 6 (#70c710)
    D 5 (#0dc571)
    L 2 (#5713f0)
    D 2 (#d2c081)
    R 2 (#59c680)
    D 2 (#411b91)
    L 5 (#8ceee2)
    U 2 (#caa173)
    L 1 (#1b58a2)
    U 2 (#caa171)
    R 2 (#7807d2)
    U 3 (#a77fa3)
    L 2 (#015232)
    U 2 (#7a21e3)
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 62, id="test-input"),
        pytest.param(REAL_INPUT, 50465, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 952408144115, id="test-input"),
        # pytest.param(REAL_INPUT, 1921197370, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
