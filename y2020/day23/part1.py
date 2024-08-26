from collections import deque
from pathlib import Path
from typing import Deque

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Deque[int]


def parse(input_str: str) -> ParsedInput:
    return deque(int(s) for s in input_str.strip())


def calculate(cups: ParsedInput, num_moves: int = 100) -> int:
    min_cup, max_cup = min(cups), max(cups)
    for move in range(num_moves):
        current_cup = cups.popleft()
        picked_up = [cups.popleft() for _ in range(3)]
        next_cup = current_cup - 1
        while True:
            if next_cup < min_cup:
                next_cup = max_cup
            elif next_cup in picked_up:
                next_cup -= 1
            else:
                break

        next_cup_index = cups.index(next_cup)
        for v in reversed(picked_up):
            cups.insert(next_cup_index + 1, v)
        cups.append(current_cup)

    # Rotate until the first value is 1
    while (first := cups.popleft()) != 1:
        cups.append(first)

    return int("".join(str(v) for v in cups))


TEST_INPUTS = [
    (
        """
        389125467
        """,
        10,
        92658374,
    ),
    (
        """
        389125467
        """,
        100,
        67384529,
    ),
]


@pytest.mark.parametrize("input_str,num_moves,expected", TEST_INPUTS)
def test(input_str: str, num_moves: int, expected: int) -> None:
    assert calculate(parse(input_str), num_moves) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
