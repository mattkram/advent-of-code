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
TEST_INPUT_3 = textwrap.dedent(
    """\
    ...........
    .S-------7.
    .|F-----7|.
    .||.....||.
    .||.....||.
    .|L-7.F-J|.
    .|..|.|..|.
    .L--J.L--J.
    ...........
    """
)
TEST_INPUT_4 = textwrap.dedent(
    """\
    .F----7F7F7F7F-7....
    .|F--7||||||||FJ....
    .||.FJ||||||||L7....
    FJL7L7LJLJ||LJ.L-7..
    L--J.L7...LJS7F-7L7.
    ....F-J..F7FJ|L7L7L7
    ....L7.F7||L7|.L7L7|
    .....|FJLJ|FJ|F7|.LJ
    ....FJL-7.||.||||...
    ....L---J.LJ.LJLJ...
    """
)
TEST_INPUT_5 = textwrap.dedent(
    """\
    FF7FSF7F7F7F7F7F---7
    L|LJ||||||||||||F--J
    FL-7LJLJ||||||LJL-77
    F--JF--7||LJLJ7F7FJ-
    L---JF-JLJ.||-FJLJJ7
    |F|F-JF---7F7-L7L|7|
    |FFJF7L7F-JF7|JL---7
    7-L-JL7||F7|L7F-7F7|
    L.L7LFJ|||||FJL7||LJ
    L7JLJL-JLJLJL--JLJ.L
    """
)

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT_1, 4, id="test-input-1"),
        pytest.param(TEST_INPUT_2, 8, id="test-input-2"),
        pytest.param(REAL_INPUT, 6942, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT_3, 4, id="test-input-3"),
        pytest.param(TEST_INPUT_4, 8, id="test-input-4"),
        pytest.param(TEST_INPUT_5, 10, id="test-input-5"),
        pytest.param(REAL_INPUT, 297, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
