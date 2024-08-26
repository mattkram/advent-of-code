from itertools import combinations
from pathlib import Path
from typing import List

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[int]


def parse(input_str: str) -> ParsedInput:
    return [int(s.strip()) for s in input_str.split() if s.strip()]


def calculate(data: ParsedInput, len_preamble: int = 25) -> int:
    for i in range(len_preamble, len(data)):
        target = data[i]
        prev_vals = data[i - len_preamble : i]
        if not any(sum(vals) == target for vals in combinations(prev_vals, 2)):
            break

    for start_ind in range(i):
        for end_ind in range(start_ind, i):
            sub_list = data[start_ind:end_ind]
            value = sum(sub_list)
            if value == target:
                return min(sub_list) + max(sub_list)
            if value > target:
                break

    raise ValueError("Cannot find an answer")


TEST_INPUTS = [
    (
        """
        35
        20
        15
        25
        47
        40
        62
        55
        65
        95
        102
        117
        150
        182
        127
        219
        299
        277
        309
        576
        """,
        62,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str), len_preamble=5) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
