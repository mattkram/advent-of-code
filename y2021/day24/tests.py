from pathlib import Path

import pytest

from .solution import calculate
from .solution import compute
from .solution import compute_manual
from .solution import parse


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize("digit", range(1, 10))
def test_compute(digit: int) -> None:
    value = "".join(str(digit) for _ in range(14))
    instructions = parse(REAL_INPUT)  # noqa: F841
    assert compute(instructions, value) == compute_manual(value)


@pytest.mark.parametrize(
    "find_max,expected",
    [
        (True, 12996997829399),
        (False, 11841231117189),
    ],
)
def test_calculate(find_max: bool, expected: int) -> None:
    assert calculate(find_max=find_max) == expected
