from pathlib import Path
from typing import List

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[List[str]]


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.splitlines()]
    group_str = "\n".join(lines).split("\n\n")
    data = [s.strip().split("\n") for s in group_str]
    return data


def calculate(data: ParsedInput) -> int:
    return sum(len(set("".join(g))) for g in data)


TEST_INPUTS = [
    (
        """
        abc

        a
        b
        c

        ab
        ac

        a
        a
        a
        a

        b
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
