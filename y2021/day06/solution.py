from pathlib import Path
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    return [int(s) for s in input_str.split(",")]


def advance(data: List[int]) -> List[int]:
    new_data = []
    num_new = 0
    for fish in data:
        if fish == 0:
            new_data.append(6)
            num_new += 1
        else:
            new_data.append(fish - 1)

    for _ in range(num_new):
        new_data.append(8)
    return new_data


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    for i in range(80):
        data = advance(data)
    return len(data)


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    for i in range(256):
        data = advance(data)
    return len(data)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
