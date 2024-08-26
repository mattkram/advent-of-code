import functools
from pathlib import Path
from typing import Set

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Set[int]


def parse(input_str: str) -> ParsedInput:
    return set(int(s.strip()) for s in input_str.split() if s.strip())


def calculate(adapters: ParsedInput) -> int:
    max_adapter = max(adapters)

    @functools.lru_cache(maxsize=None)
    def get_num_routes(target: int = 0) -> int:
        if target == max_adapter:
            return 1

        return sum(
            get_num_routes(new_target)
            for new_target in range(target + 1, target + 4)
            if new_target in adapters
        )

    return get_num_routes()


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
