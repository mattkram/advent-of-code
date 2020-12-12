from pathlib import Path
from typing import Dict
from typing import Set

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Set[int]


def parse(input_str: str) -> ParsedInput:
    return {int(s.strip()) for s in input_str.split() if s.strip()}


def calculate(adapters: ParsedInput) -> int:
    adapters = set(adapters)
    jumps: Dict[int, int] = {}

    jolts = 0
    while adapters:
        for i in range(1, 4):
            try:
                adapters.remove(jolts + i)
            except KeyError:
                pass
            else:
                jolts += i
                jumps[i] = jumps.get(i, 0) + 1
                break
    jolts += 3
    jumps[3] += 1

    return jumps[1] * jumps[3]


TEST_INPUTS = [
    (
        """
        16
        10
        15
        5
        1
        11
        7
        19
        6
        12
        4
        """,
        35,
    ),
    (
        """
        28
        33
        18
        42
        31
        14
        46
        20
        48
        47
        24
        23
        49
        45
        19
        38
        39
        11
        1
        32
        25
        35
        8
        17
        7
        9
        4
        2
        34
        10
        3
        """,
        220,
    ),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
