from pathlib import Path
from typing import Tuple

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Tuple[int, int]


def parse(input_str: str) -> ParsedInput:
    line_1, line_2 = input_str.strip().splitlines()
    return int(line_1), int(line_2)


def handshake(
    subject_number: int, loop_size: int, *, target: int = None, divisor: int = 20201227
) -> int:
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value %= divisor
        if value == target:
            return i + 1
    return value


def calculate(data: ParsedInput) -> int:
    card_public_key, door_public_key = data

    card_loop_size = handshake(7, 1_000_000_000, target=card_public_key)
    door_loop_size = handshake(7, 1_000_000_000, target=door_public_key)

    card_encryption_key = handshake(card_public_key, door_loop_size)
    door_encryption_key = handshake(door_public_key, card_loop_size)

    assert card_encryption_key == door_encryption_key

    return card_encryption_key


TEST_INPUTS = [
    (
        """
        5764801
        17807724
        """,
        14897079,
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
