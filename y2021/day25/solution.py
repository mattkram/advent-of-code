from pathlib import Path
from typing import Dict, Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Tuple[Dict[Tuple[int, int], str], Tuple[int, int]]:
    data = {}
    row = 0
    for line in input_str.splitlines():
        if not line.strip():
            continue
        num_cols = len(line.strip())
        for col, char in enumerate(line.strip()):
            if char != ".":
                data[row, col] = char

        row += 1
        num_rows = row
    return data, (num_rows, num_cols)


def calculate_part1(input_str: str) -> int:
    data, (num_rows, num_cols) = parse(input_str)  # noqa: F841
    it = 0
    while True:
        changed = False
        new_data = {}
        for (row, col), char in data.items():
            if char == ">":
                if data.get((row, (col + 1) % num_cols)) is None:
                    changed = True
                    new_data[row, (col + 1) % num_cols] = char
                else:
                    new_data[row, col] = char
            else:
                new_data[row, col] = char

        data = new_data.copy()
        new_data = {}
        for (row, col), char in data.items():
            if char == "v":
                if data.get(((row + 1) % num_rows, col)) is None:
                    changed = True
                    new_data[(row + 1) % num_rows, col] = char
                else:
                    new_data[row, col] = char
            else:
                new_data[row, col] = char

        data = new_data.copy()
        it += 1

        if not changed:
            break

    return it


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")


if __name__ == "__main__":
    main()
