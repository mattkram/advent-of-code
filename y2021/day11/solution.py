import itertools
from pathlib import Path
from typing import Dict
from typing import Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Dict[Tuple[int, int], int]:
    data = {}
    for i, line in enumerate(input_str.strip().split()):
        for j, char in enumerate(line.strip()):
            data[i, j] = int(char)

    return data


def take_step(data: Dict[Tuple[int, int], int]) -> int:
    for pos in data:
        data[pos] += 1
    blinked = set()
    while any(i > 9 for i in data.values()):
        for pos in dict(data):
            if data[pos] > 9 and pos not in blinked:
                blinked.add(pos)
                data.pop(pos)
                for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
                    new_pos = (pos[0] + dx, pos[1] + dy)
                    if new_pos in data:
                        data[new_pos] += 1
    for pos in blinked:
        data[pos] = 0
    return len(blinked)


def calculate_part1(input_str: str, num_steps: int) -> int:
    data = parse(input_str)  # noqa: F841
    num_blinked = 0
    for step in range(num_steps):
        num_blinked += take_step(data)

    return num_blinked


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    iteration = 0
    while True:
        take_step(data)
        iteration += 1
        if all(i == 0 for i in data.values()):
            return iteration


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str, num_steps=100)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
