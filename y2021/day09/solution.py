import math
from pathlib import Path
from typing import List, Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[List[int]]:
    return [[int(i) for i in list(s.strip())] for s in input_str.split() if s.strip()]


def find_low_points(data: List[List[int]]) -> List[Tuple[int, int]]:
    low_points = []
    num_rows = len(data)
    num_cols = len(data[0])
    for row in range(num_rows):
        for col in range(num_cols):
            neighbors = []
            if col > 0:
                neighbors.append(data[row][col - 1])
            if row > 0:
                neighbors.append(data[row - 1][col])
            if col < num_cols - 1:
                neighbors.append(data[row][col + 1])
            if row < num_rows - 1:
                neighbors.append(data[row + 1][col])
            if all(data[row][col] < n for n in neighbors):
                low_points.append((row, col))
    return low_points


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    low_points = find_low_points(data)
    return sum(data[row][col] + 1 for row, col in low_points)


def get_num_basin_points(data: List[List[int]], point: Tuple[int, int]) -> int:
    basin_points = {point}
    num_rows = len(data)
    num_cols = len(data[0])
    has_new_points = True
    while has_new_points:
        has_new_points = False
        for row, col in set(basin_points):
            for d_row, d_col in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                neighbor_pos = (row + d_row, col + d_col)
                if not (
                    0 <= neighbor_pos[0] <= num_rows - 1
                    and 0 <= neighbor_pos[1] <= num_cols - 1
                ):
                    continue

                neighbor_value = data[neighbor_pos[0]][neighbor_pos[1]]
                if neighbor_value < 9 and neighbor_pos not in basin_points:
                    basin_points.add(neighbor_pos)
                    has_new_points = True
    return len(basin_points)


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    low_points = find_low_points(data)
    return math.prod(
        sorted((get_num_basin_points(data, pt) for pt in low_points), reverse=True)[:3]
    )


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
