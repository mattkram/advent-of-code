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
    "input_str,expected,num_steps",
    [
        (TEST_INPUT, 1588, 10),
        (REAL_INPUT, 3118, 10),
        (TEST_INPUT, 2188189693529, 40),
        (REAL_INPUT, 4332887448171, 40),
    ],
)
def test_calculate(input_str: str, expected: int, num_steps: int) -> None:
    assert calculate(input_str, num_steps=num_steps) == expected
