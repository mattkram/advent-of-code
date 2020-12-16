from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Tuple[int, List[Optional[int]]]


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.split() if s.strip()]
    earliest_timestamp = int(lines[0])
    buses = [int(s) if s != "x" else None for s in lines[1].split(",")]
    return earliest_timestamp, buses


def calculate(data: ParsedInput) -> int:
    _, buses = data

    bus_list = [(i, bus) for i, bus in enumerate(buses) if bus is not None]
    print(bus_list)

    t = 0
    dt = bus_list[0][1]  # max(bus for bus in bus_dict.values())
    while True:
        if all((t + i) % bus == 0 for i, bus in bus_list):
            break
        t += dt
    return (t // dt) * dt


TEST_INPUTS = [
    (
        """
        0
        7,13,x,x,59,x,31,19
        """,
        1068781,
    ),
    (
        """
        0
        17,x,13,19
        """,
        3417,
    ),
    (
        """
        0
        67,7,59,61
        """,
        754018,
    ),
    (
        """
        0
        67,x,7,59,61
        """,
        779210,
    ),
    (
        """
        0
        67,7,x,59,61
        """,
        1261476,
    ),
    (
        """
        0
        1789,37,47,1889
        """,
        1202161486,
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
