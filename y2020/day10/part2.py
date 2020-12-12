from pathlib import Path
from typing import Dict
from typing import List

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[int]


def parse(input_str: str) -> ParsedInput:
    return [0] + sorted(int(s.strip()) for s in input_str.split() if s.strip())


def calculate(
    adapters: ParsedInput, index: int = 0, target: int = 0, cache: Dict[int, int] = None
) -> int:

    if cache is None:
        cache = {}

    try:
        return cache[index]
    except KeyError:
        pass

    if adapters[index] == adapters[-1]:
        total = 1
    else:
        smallest_step = adapters[index + 1] - target

        total = 0
        for i in range(smallest_step, 4):
            new_target = target + i
            try:
                new_index = adapters[index : index + 4].index(new_target) + index
            except ValueError:
                pass
            else:
                total += calculate(adapters, new_index, new_target, cache)

    cache[index] = total
    return total


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
        8,
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
        19208,
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
