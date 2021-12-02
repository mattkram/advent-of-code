from pathlib import Path
from typing import List
from typing import Tuple


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[Tuple[str, int]]:
    result = []
    for line in input_str.splitlines():
        if not line.strip():
            continue
        direction, value = line.split()
        result.append((direction, int(value)))
    return result


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)
    x, z = 0, 0
    for direction, value in data:
        if direction == "forward":
            x += value
        elif direction == "down":
            z += value
        elif direction == "up":
            z -= value
        else:
            raise ValueError
    return x * z


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)
    horizontal, depth, aim = 0, 0, 0
    for direction, value in data:
        if direction == "forward":
            horizontal += value
            depth += aim * value
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value
        else:
            raise ValueError
    return horizontal * depth


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
