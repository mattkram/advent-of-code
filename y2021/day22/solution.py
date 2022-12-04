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
            rf"(\w+) x={NUM}..{NUM},y={NUM}..{NUM},z={NUM}..{NUM}", line.strip()
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
    instructions = parse(input_str)  # noqa: F841

    x_lim_set = set()
    y_lim_set = set()
    z_lim_set = set()
    for turn_on, x_min_i, x_max_i, y_min_i, y_max_i, z_min_i, z_max_i in instructions:
        x_lim_set.add(x_min_i - 0.5)
        x_lim_set.add(x_max_i + 0.5)
        y_lim_set.add(y_min_i - 0.5)
        y_lim_set.add(y_max_i + 0.5)
        z_lim_set.add(z_min_i - 0.5)
        z_lim_set.add(z_max_i + 0.5)

    x_lims = sorted(x_lim_set)
    y_lims = sorted(y_lim_set)
    z_lims = sorted(z_lim_set)

    s = 0
    for x_min, x_max in zip(x_lims, x_lims[1:]):
        filtered_x = [
            (turn_on, x_min_i, x_max_i, y_min_i, y_max_i, z_min_i, z_max_i)
            for turn_on, x_min_i, x_max_i, y_min_i, y_max_i, z_min_i, z_max_i in instructions
            if x_min_i <= int(x_min + 0.5) <= x_max_i
        ]
        if not filtered_x:
            continue
        for y_min, y_max in zip(y_lims, y_lims[1:]):
            filtered_y = [
                (turn_on, x_min_i, x_max_i, y_min_i, y_max_i, z_min_i, z_max_i)
                for turn_on, x_min_i, x_max_i, y_min_i, y_max_i, z_min_i, z_max_i in filtered_x
                if y_min_i <= int(y_min + 0.5) <= y_max_i
            ]
            if not filtered_y:
                continue
            for z_min, z_max in zip(z_lims, z_lims[1:]):
                filtered_z = [
                    (turn_on, x_min_i, x_max_i, y_min_i, y_max_i, z_min_i, z_max_i)
                    for turn_on, x_min_i, x_max_i, y_min_i, y_max_i, z_min_i, z_max_i in filtered_y
                    if z_min_i <= int(z_min + 0.5) <= z_max_i
                ]
                if not filtered_z:
                    continue

                turn_on, *_ = filtered_z[-1]
                if turn_on:
                    s += int((x_max - x_min) * (y_max - y_min) * (z_max - z_min))

    return s


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
