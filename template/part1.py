from pathlib import Path
from typing import List

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[int]


def parse(input_str: str) -> ParsedInput:
    return [int(s.strip()) for s in input_str.split() if s.strip()]


def calculate(data: ParsedInput) -> int:
    raise ValueError("Cannot find an answer")


TEST_INPUTS = [
    (
        """
        some_input
        abc
        """,
        11,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
