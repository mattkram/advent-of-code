from pathlib import Path
from typing import List
from typing import Tuple

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Tuple[int, List[int]]


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.split() if s.strip()]
    earliest_timestamp = int(lines[0])
    buses = [int(s) for s in lines[1].split(",") if s != "x"]
    return earliest_timestamp, buses


def calculate(data: ParsedInput) -> int:
    arrival, buses = data

    wait_time = [(arrival // bus + 1) * bus - arrival for bus in buses]

    min_wait = min(wait_time)
    next_bus = buses[wait_time.index(min_wait)]
    return min_wait * next_bus


TEST_INPUTS = [
    (
        """
        939
        7,13,x,x,59,x,31,19
        """,
        295,
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
