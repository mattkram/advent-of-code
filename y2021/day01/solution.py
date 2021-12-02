from pathlib import Path
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    return [int(s.strip()) for s in input_str.split() if s.strip()]


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)
    return sum(next_ > first for first, next_ in zip(data, data[1:]))


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)
    moving_sum = [sum(data[i : i + 3]) for i in range(len(data) - 2)]
    return sum(next_ > first for first, next_ in zip(moving_sum, moving_sum[1:]))


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
