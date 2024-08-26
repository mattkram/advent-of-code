import math
from pathlib import Path
from typing import List, Tuple

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[Tuple[str, int]]


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.split() if s.strip()]
    return [(s[0], int(s[1:])) for s in lines]


def calculate(instructions: ParsedInput) -> int:
    pos_E, pos_N = (0, 0)
    dir_E, dir_N = (1, 0)

    for key, val in instructions:
        if key == "N":
            pos_N += val
        elif key == "S":
            pos_N -= val
        elif key == "E":
            pos_E += val
        elif key == "W":
            pos_E -= val
        elif key in "RL":
            ang = (val if key == "L" else -val) * math.pi / 180
            C, S = math.cos(ang), math.sin(ang)
            dir_E, dir_N = (int(C * dir_E - S * dir_N), int(S * dir_E + C * dir_N))
        elif key == "F":
            pos_E += val * dir_E
            pos_N += val * dir_N
        else:
            raise ValueError(f"Invalid instruction: {key}")

    return abs(pos_E) + abs(pos_N)


TEST_INPUTS = [
    (
        """
        F10
        N3
        F7
        R90
        F11
        """,
        25,
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
