from pathlib import Path
from typing import List

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[str]:
    return [s.strip() for s in input_str.split() if s.strip()]


def find_most_common(data: List[str], input_char: str) -> int:
    """Find the most common bit in each position, and then return as an integer."""
    data = list(data)
    first, *_ = data
    num_cols = len(first)
    num_lines = len(data)
    sums = [0 for _ in range(num_cols)]
    for line in data:
        for i, char in enumerate(line):
            sums[i] += char == input_char

    # Tells you if 1 is more or less common
    most_common = [f"{int(sums[i] >= num_lines / 2):d}" for i in range(num_cols)]
    x = int("".join(most_common), 2)
    return x


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)
    return find_most_common(data, "1") * find_most_common(data, "0")


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)
    first, *_ = data
    num_cols = len(first)

    new_data = list(data)
    for i in range(num_cols):
        if len(new_data) == 1:
            break

        most_common_string = f'{find_most_common(new_data, "1"):0{num_cols}b}'
        new_data = [line for line in new_data if line[i] == most_common_string[i]]

    oxygen = int(new_data[0], 2)

    new_data = list(data)
    for i in range(num_cols):
        if len(new_data) == 1:
            break

        most_common_string = f'{find_most_common(new_data, "1"):0{num_cols}b}'
        most_common_string = "".join(
            "0" if s == "1" else "1" for s in most_common_string
        )
        new_data = [line for line in new_data if line[i] == most_common_string[i]]

    co2 = int(new_data[0], 2)

    return oxygen * co2


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
