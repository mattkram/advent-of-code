import itertools
import re
from pathlib import Path
from typing import List
from typing import Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"
NUM = r"(-?\d+)"

Instruction = Tuple[bool, int, int, int, int, int, int]


def parse(input_str: str) -> List[Instruction]:
    instructions: List[Instruction] = []
    for line in input_str.strip().splitlines():
        if m := re.match(
            fr"(\w+) x={NUM}..{NUM},y={NUM}..{NUM},z={NUM}..{NUM}", line.strip()
        ):
            on_off, *values = m.groups()
            x_min, x_max, y_min, y_max, z_min, z_max = (int(v) for v in values)
            instructions.append(
                (on_off == "on", x_min, x_max, y_min, y_max, z_min, z_max)
            )
    return instructions


def calculate_part1(input_str: str) -> int:
    instructions = parse(input_str)  # noqa: F841
    cells = set()

    for turn_on, x_min, x_max, y_min, y_max, z_min, z_max in instructions:
        x_min = max(x_min, -50)
        x_max = min(x_max, 50)
        y_min = max(y_min, -50)
        y_max = min(y_max, 50)
        z_min = max(z_min, -50)
        z_max = min(z_max, 50)
        subcells = set(
            itertools.product(
                range(x_min, x_max + 1),
                range(y_min, y_max + 1),
                range(z_min, z_max + 1),
            )
        )
        if turn_on:
            cells |= subcells
        else:
            cells -= subcells

    return len(cells)


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    raise ValueError("Cannot find an answer")


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
