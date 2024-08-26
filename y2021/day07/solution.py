from pathlib import Path
from typing import List

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    return [int(s.strip()) for s in input_str.split(",")]


def get_distance(positions: List[int], pos: int) -> int:
    return sum(abs(i) for i in positions)


def calculate_part1(input_str: str) -> int:
    positions = parse(input_str)  # noqa: F841
    return min(
        sum(abs(pos - i) for i in positions) for pos in range(max(positions) + 1)
    )


def calculate_part2(input_str: str) -> int:
    positions = parse(input_str)  # noqa: F841
    return min(
        sum(abs(pos - i) * (abs(pos - i) + 1) // 2 for i in positions)
        for pos in range(max(positions) + 1)
    )


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
