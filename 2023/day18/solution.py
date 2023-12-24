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


def calculate_area(points: list[tuple[int, int]]) -> int:
    """Calculate the area of a polygon, assuming points oriented clockwise"""
    area = 0
    for (x_0, y_0), (x_1, y_1) in zip(points, points[1:]):
        area += (x_1 - x_0) * (y_0 + y_1) // 2
    return area


TURN_MAP = {
    ("R", "D"): "expand",
    ("R", "U"): "contract",
    ("D", "L"): "expand",
    ("D", "R"): "contract",
    ("L", "U"): "expand",
    ("L", "D"): "contract",
    ("U", "R"): "expand",
    ("U", "L"): "contract",
}


def calculate_area_from_steps(steps):
    position = (0, 0)
    trench = [position]
    print()
    prev_ec = "expand"
    for step, next_step in zip(steps, steps[1:] + [steps[0]]):
        delta = DIRECTION_MAP[step.direction]

        ec = TURN_MAP[step.direction, next_step.direction]

        distance = step.distance
        if ec == "expand":
            distance += 1
        if prev_ec == "contract":
            distance -= 1
        prev_ec = ec

        position = (
            position[0] + distance * delta[0],
            position[1] + distance * delta[1],
        )
        trench.append(position)

    return calculate_area(trench)


def calculate_part1(input_str: str) -> int:
    steps = parse(input_str)
    return calculate_area_from_steps(steps)

    position = (0, 0)
    trench = [position]
    print()
    prev_ec = "expand"
    for step, next_step in zip(steps, steps[1:] + [steps[0]]):
        delta = DIRECTION_MAP[step.direction]

        ec = TURN_MAP[step.direction, next_step.direction]

        distance = step.distance
        if ec == "expand":
            distance += 1
        if prev_ec == "contract":
            distance -= 1
        prev_ec = ec

        position = (
            position[0] + distance * delta[0],
            position[1] + distance * delta[1],
        )
        trench.append(position)

    return calculate_area(trench)
    num_interior = count_interior_tiles(trench)
    return len(set(trench)) + num_interior


HIDDEN_DIRECTION_MAP = {0: "R", 1: "D", 2: "L", 3: "U"}


def derive_encoded_steps(steps: list[Step]) -> list[Step]:
    new_steps = []

    for step in steps:
        color = step.color
        direction = HIDDEN_DIRECTION_MAP[int(color[5])]
        distance = int(step.color[:5], 16)
        new_steps.append(Step(direction, distance, color))

    return new_steps


def calculate_part2(input_str: str) -> int:
    steps = parse(input_str)

    steps = derive_encoded_steps(steps)
    return calculate_area_from_steps(steps)

    position = (0, 0)
    trench = [position]
    for step in steps:
        delta = DIRECTION_MAP[step.direction]
        position = (
            position[0] + step.distance * delta[0],
            position[1] + step.distance * delta[1],
        )
        trench.append(position)

    return calculate_area(trench)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
