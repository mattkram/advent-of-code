from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).parents[1]


def parse_data(lines: list[str]) -> list[list[int]]:
    data = []
    for line in lines:
        data.append([int(c) for c in line])
    return data


def mark_visible(
    data: list[list[int]], visible: list[list[bool]]
) -> tuple[list[list[int]], list[list[bool]]]:
    """Mutably mark the visible list by evaluating each row.
    The data list will come in transposed, reversed, etc.
    """
    for i, row in enumerate(data):
        for j, height in enumerate(row):
            # Note: all([]) -> True
            if all(height > v for v in row[:j]):
                visible[i][j] = True
    return data, visible


def solve_part1() -> int:
    path = Path("data", "day08.txt")
    with path.open() as fp:
        lines = [line.strip() for line in fp]

    data = parse_data(lines)
    visible_trees = [[False for _ in row] for row in data]

    # Original orientation (left-to-right)
    mark_visible(data, visible_trees)

    # Flip horizontally (right-to-left)
    data = [list(reversed(row)) for row in data]
    visible_trees = [list(reversed(row)) for row in visible_trees]
    data, visible_trees = mark_visible(data, visible_trees)

    # Transpose (top-to-bottom)
    data = [list(s) for s in list(zip(*data))]
    visible_trees = [list(s) for s in list(zip(*visible_trees))]
    data, visible_trees = mark_visible(data, visible_trees)

    # Flip horizontally again (bottom-to-top)
    data = [list(reversed(row)) for row in data]
    visible_trees = [list(reversed(row)) for row in visible_trees]
    data, visible_trees = mark_visible(data, visible_trees)

    return sum(sum(row) for row in visible_trees)


def solve_part2() -> int:
    path = Path("data", "day08.txt")
    with path.open() as fp:
        lines = [line.strip() for line in fp]

    data = parse_data(lines)

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    num_rows = len(data)
    num_cols = len(data[0])

    max_scenic_score = 0
    for row in range(1, num_rows - 1):
        for col in range(1, num_cols - 1):
            base_pos = (row, col)
            base_ht = data[row][col]
            distances = []
            for d in directions:
                dist = 1
                while True:
                    pos = (base_pos[0] + dist * d[0], base_pos[1] + dist * d[1])
                    if (
                        pos[0] <= 0
                        or pos[1] <= 0
                        or pos[0] >= num_rows - 1
                        or pos[1] >= num_cols - 1
                    ):
                        break
                    ht = data[pos[0]][pos[1]]
                    if ht >= base_ht:
                        break
                    dist += 1
                distances.append(dist)
            scenic_score = distances[0] * distances[1] * distances[2] * distances[3]
            max_scenic_score = max(scenic_score, max_scenic_score)
    return max_scenic_score

    return 0


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
