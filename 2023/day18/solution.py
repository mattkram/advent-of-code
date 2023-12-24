import re
from pathlib import Path
from typing import NamedTuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


DIRECTION_MAP = {
    "U": (0, +1),
    "R": (+1, 0),
    "D": (0, -1),
    "L": (-1, 0),
}


class Step(NamedTuple):
    direction: str
    distance: int
    color: str


def parse(input_str: str) -> list[int]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    steps = []
    for line in lines:
        pattern = re.compile(r"(\w) (\d+) \(#(\w+)\)")
        if m := pattern.match(line):
            direction = m.group(1)
            distance = int(m.group(2))
            color = m.group(3)
            steps.append(Step(direction, distance, color))
        else:
            raise ValueError(f"Couldn't parse line {line}")
    return steps


def count_interior_tiles(path):
    loop = set(path)  # Used to more efficiently check membership
    enclosed = set()

    for curr, next in zip(path, path[1:]):
        (dx, dy) = (next[0] - curr[0], next[1] - curr[1])

        # 90 deg, counter-clockwise
        search_dir = dy, -dx

        # Search in that direction until we hit a part of the loop
        # We need to search from both the current and next location
        # This covers corners, where the direction will change and
        # next -> curr.
        for xy in [curr, next]:
            while (xy := (xy[0] + search_dir[0], xy[1] + search_dir[1])) not in loop:
                enclosed.add(xy)
                if max(max(xy), abs(min(xy))) > 1000:
                    # If we go off the board, we need to go the other way through the loop
                    return count_interior_tiles(path[::-1])

    return len(enclosed)


def calculate_part1(input_str: str) -> int:
    steps = parse(input_str)

    position = (0, 0)
    trench = [position]
    for step in steps:
        delta = DIRECTION_MAP[step.direction]
        for d in range(1, step.distance + 1):
            position = (position[0] + delta[0], position[1] + delta[1])
            trench.append(position)

    num_interior = count_interior_tiles(trench)
    return len(set(trench)) + num_interior


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
