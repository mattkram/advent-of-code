import math
from itertools import combinations
from pathlib import Path

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"


def calculate(input_str: str) -> int:
    values = [int(s) for s in input_str.split()]
    for subset in combinations(values, 3):
        if sum(subset) == 2020:
            return math.prod(subset)
    raise ValueError("Cannot find an answer")


TEST_INPUTS = [
    (
        """
        1721
        979
        366
        299
        675
        1456
        """,
        241861950,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(fp.read())


if __name__ == "__main__":
    print(f"The answer is {main()}")
