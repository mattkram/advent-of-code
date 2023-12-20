import itertools
from pathlib import Path
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    galaxies = set()

    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == "#":
                galaxies.add((i, j))

    return galaxies


def find_expansions(galaxies: set[tuple[int, int]]) -> tuple[set[int], set[int]]:
    min_row = min(g[1] for g in galaxies)
    max_row = max(g[1] for g in galaxies)
    min_col = min(g[0] for g in galaxies)
    max_col = max(g[0] for g in galaxies)

    rows, cols = set(), set()

    for row in range(min_row, max_row + 1):
        if not any(row == g[1] for g in galaxies):
            rows.add(row)

    for col in range(min_col, max_col + 1):
        if not any(col == g[0] for g in galaxies):
            cols.add(col)

    return rows, cols


def calculate_part1(input_str: str) -> int:
    galaxies = parse(input_str)
    expansion_rows, expansion_cols = find_expansions(galaxies)

    result = 0
    for a, b in itertools.combinations(galaxies, 2):
        x_min = min(a[0], b[0])
        x_max = max(a[0], b[0])
        y_min = min(a[1], b[1])
        y_max = max(a[1], b[1])
        dx = x_max - x_min
        dy = y_max - y_min

        # Manhattan distance
        dist = dx + dy

        # Add extra for each expanding row or column in the range
        for x in range(x_min, x_max + 1):
            if x in expansion_cols:
                dist += 1

        for y in range(y_min, y_max + 1):
            if y in expansion_rows:
                dist += 1

        result += dist
    return result


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
