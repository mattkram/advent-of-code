from collections import Counter
from pathlib import Path
from typing import List

INPUTS_FILE = Path(__file__).parent / "input.txt"


def int_to_bit_str(num: int, length: int = 0) -> str:
    return f"{num:0{length}b}"


def bit_str_to_ints(string: str) -> List[int]:
    return [int(s) for s in string]


def flip_bits(num: int, count: int) -> int:
    """Flip the right-most `count` bits in an integer."""
    mask = ~(~0 >> count << count)
    return num ^ mask


def parse(input_str: str) -> List[str]:
    return [s.strip() for s in input_str.split() if s.strip()]


def find_most_common(data: List[str], tiebreak_bit: int) -> int:
    """Find the most common bit in each position, and then return as an integer."""
    # Convert each string to a list of ints
    int_data = [bit_str_to_ints(line) for line in data]

    result = 0
    for col in zip(*int_data):
        # Count occurrences of each bit in each column
        c = Counter(col)
        result <<= 1
        result |= c[tiebreak_bit] >= c[not tiebreak_bit]

    return result


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)
    num_cols = len(data[0])
    return find_most_common(data, 1) * flip_bits(find_most_common(data, 1), num_cols)


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)
    first, *_ = data
    num_cols = len(first)

    new_data = list(data)
    for i in range(num_cols):
        if len(new_data) == 1:
            break

        most_common = find_most_common(new_data, 1)
        most_common_string = int_to_bit_str(most_common, num_cols)
        new_data = [line for line in new_data if line[i] == most_common_string[i]]

    oxygen = int(new_data[0], 2)

    new_data = list(data)
    for i in range(num_cols):
        if len(new_data) == 1:
            break

        most_common = flip_bits(find_most_common(new_data, 1), num_cols)
        most_common_string = int_to_bit_str(most_common, num_cols)
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
