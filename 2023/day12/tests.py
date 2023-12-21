import textwrap
from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT = textwrap.dedent(
    """\
    ???.### 1,1,3
    .??..??...?##. 1,1,3
    ?#?#?#?#?#?#?#? 1,3,1,6
    ????.#...#... 4,1,1
    ????.######..#####. 1,6,5
    ?###???????? 3,2,1
    """
)


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param("#.#.### 1,1,3", 1),
        pytest.param(TEST_INPUT.splitlines()[0], 1),
        pytest.param(TEST_INPUT.splitlines()[1], 4),
        pytest.param(TEST_INPUT.splitlines()[2], 1),
        pytest.param(TEST_INPUT.splitlines()[3], 1),
        pytest.param(TEST_INPUT.splitlines()[4], 4),
        pytest.param(TEST_INPUT.splitlines()[5], 10),
        (".###..##.??? 3,2,1", 3),
        (".###..##..?? 3,2,1", 2),
        (".###..##..?. 3,2,1", 1),
        (".###..##...? 3,2,1", 1),
        (".###.##.???? 3,2,1", 4),
        (".###.#.#.#.. 3,2,1", 0),
        ("?###???????? 3,2,1", 10),
        pytest.param(TEST_INPUT, 21, id="test-input"),
        pytest.param(REAL_INPUT, 7718, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 525152, id="test-input"),
        pytest.param(REAL_INPUT, 128741994134728, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
