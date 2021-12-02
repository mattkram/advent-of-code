from pathlib import Path
from typing import List
from typing import Tuple

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[Tuple[str, int]]


def parse(input_str: str) -> ParsedInput:
    result = []
    for line in input_str.splitlines():
        if not line.strip():
            continue
        direction, value = line.split()
        result.append((direction, int(value)))
    return result


def calculate(data: ParsedInput) -> int:
    x, z = 0, 0
    for direction, value in data:
        if direction == "forward":
            x += value
        elif direction == "down":
            z += value
        elif direction == "up":
            z -= value
        else:
            raise ValueError
    return x * z


TEST_INPUTS = [
    (
        """
        forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2
        """,
        150,
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
