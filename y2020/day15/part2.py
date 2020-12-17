from pathlib import Path
from typing import List

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[int]


def parse(input_str: str) -> ParsedInput:
    return [int(s.strip()) for s in input_str.split(",") if s.strip()]


def calculate(data: ParsedInput) -> int:
    record = {num: last_said for last_said, num in enumerate(data[:-1])}

    next_spoken = data[-1]
    for i in range(len(record), 30000000):
        last_spoken = next_spoken

        try:
            next_spoken = i - record[last_spoken]
        except KeyError:
            next_spoken = 0

        record[last_spoken] = i

    return last_spoken


TEST_INPUTS = [
    ("0,3,6", 175594),
    ("1,3,2", 2578),
    ("2,1,3", 3544142),
    ("1,2,3", 261214),
    ("2,3,1", 6895259),
    ("3,2,1", 18),
    ("3,1,2", 362),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
