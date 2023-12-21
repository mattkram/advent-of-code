from pathlib import Path
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    map = {}
    positions = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                map[row, col] = char
            elif char == "S":
                positions.add((row, col))

    return positions, map


def move(coords, map):
    """Move the given coords in four directions, returning"""
    result = set()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_coords = coords[0] + dx, coords[1] + dy
        if map.get(new_coords, ".") != "#":
            result.add(new_coords)
    return result


def calculate_part1(input_str: str, num_steps: int) -> int:
    positions, map = parse(input_str)  # noqa: F841

    for _ in range(num_steps):
        new_positions = [move(p, map) for p in positions]
        positions = set()
        for p in new_positions:
            positions.update(p)
    return len(positions)


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
