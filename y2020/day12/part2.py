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
    pos_E, pos_N = (0, 0)  # ship position
    wpt_E, wpt_N = (10, 1)  # waypoint position

    for key, val in instructions:
        if key == "N":
            wpt_N += val
        elif key == "S":
            wpt_N -= val
        elif key == "E":
            wpt_E += val
        elif key == "W":
            wpt_E -= val
        elif key in "RL":
            ang = (val if key == "L" else -val) * math.pi / 180
            C, S = round(math.cos(ang)), round(math.sin(ang))
            wpt_E, wpt_N = (C * wpt_E - S * wpt_N, S * wpt_E + C * wpt_N)
        elif key == "F":
            pos_E += val * wpt_E
            pos_N += val * wpt_N
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
        286,
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
