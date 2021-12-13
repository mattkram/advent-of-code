from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2

TEST_INPUT_1 = """
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
"""

TEST_INPUT_2 = """
    dc-end
    HN-start
    start-kj
    dc-start
    dc-HN
    LN-dc
    HN-end
    kj-sa
    kj-HN
    kj-dc
"""

TEST_INPUT_3 = """
    fs-end
    he-DX
    fs-he
    start-DX
    pj-DX
    end-zg
    zg-sl
    zg-pj
    pj-he
    RW-he
    fs-DX
    pj-RW
    zg-RW
    start-pj
    he-WI
    zg-he
    pj-fs
    start-RW
"""

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT_1, 10),
        (TEST_INPUT_2, 19),
        (TEST_INPUT_3, 226),
        (REAL_INPUT, 4912),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT_1, 36),
        (TEST_INPUT_2, 103),
        (TEST_INPUT_3, 3509),
        (REAL_INPUT, 150004),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
