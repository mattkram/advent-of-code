from collections import Counter
from pathlib import Path
from typing import List, Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def int_to_bit_str(num: int, length: int = 0) -> str:
    return f"{num:0{length}b}"


def bit_str_to_ints(string: str) -> List[int]:
    return [int(s) for s in string]


def flip_bits(num: int, count: int) -> int:
    """Flip the right-most `count` bits in an integer."""
    mask = ~(~0 >> count << count)
    return num ^ mask


def extract_bit(num: int, shift: int) -> int:
    """Extract a bit `shift` positions from the right."""
    return (num >> shift) & 1


def parse(input_str: str) -> Tuple[List[str], int]:
    lines = [s.strip() for s in input_str.split() if s.strip()]
    return lines, len(lines[0])


def find_most_common(data: List[str]) -> int:
    """Find the most common bit in each position, and then return as an integer."""
    # Convert each string to a list of ints
    int_data = [bit_str_to_ints(line) for line in data]

    result = 0
    for col in zip(*int_data):
        # Count occurrences of each bit in each column
        c = Counter(col)
        result <<= 1
        result |= c[1] >= c[0]

    return result


def calculate_part1(input_str: str) -> int:
    data, num_cols = parse(input_str)
    return find_most_common(data) * flip_bits(find_most_common(data), num_cols)


def calculate_part2(input_str: str) -> int:
    data, num_cols = parse(input_str)

    new_data = list(data)
    shift = num_cols - 1
    while len(new_data) > 1 and shift >= 0:
        most_common = find_most_common(new_data)
        most_common_bit = extract_bit(most_common, shift)

        new_data = [
            line
            for line in new_data
            if extract_bit(int(line, 2), shift) == most_common_bit
        ]
        shift -= 1

    oxygen = int(new_data[0], 2)

    new_data = list(data)
    shift = num_cols - 1
    while len(new_data) > 1 and shift >= 0:
        most_common = flip_bits(find_most_common(new_data), num_cols)
        most_common_bit = extract_bit(most_common, shift)

        new_data = [
            line
            for line in new_data
            if extract_bit(int(line, 2), shift) == most_common_bit
        ]
        shift -= 1

    co2 = int(new_data[0], 2)

    return oxygen * co2


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
