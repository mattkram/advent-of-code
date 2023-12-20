from pathlib import Path
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    series = [[int(i) for i in line.split()] for line in lines]
    return series


def predict_next(series: list[int]) -> int:
    stack = [series[-1]]

    diffs = series
    while True:
        diffs = [b - a for a, b in zip(diffs, diffs[1:])]

        if all(d == 0 for d in diffs):
            stack.append(0)
            break

        last_element = diffs[-1]
        stack.append(last_element)

    return sum(stack)


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    return sum(predict_next(series) for series in data)


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
