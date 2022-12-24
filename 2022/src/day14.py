from __future__ import annotations

from pathlib import Path

START = (500, 0)

BASE_DIR = Path(__file__).parents[1]


def load_input() -> set[tuple[int, int]]:
    path = Path("data", "day14.txt")
    rocks = set()
    with path.open() as fp:
        for line in fp:
            if not line.strip():
                continue
            coord_strings = line.strip().split(" -> ")
            coords = [tuple(int(i) for i in s.split(",")) for s in coord_strings]
            for start, end in zip(coords, coords[1:]):
                dx = end[0] - start[0]
                dy = end[1] - start[1]
                if dx == 0:
                    x = start[0]
                    if dy > 0:
                        for y in range(start[1], end[1] + 1):
                            rocks.add((x, y))
                    else:
                        for y in range(start[1], end[1] - 1, -1):
                            rocks.add((x, y))
                else:
                    y = start[1]
                    if dx > 0:
                        for x in range(start[0], end[0] + 1, 1):
                            rocks.add((x, y))
                    else:
                        for x in range(start[0], end[0] - 1, -1):
                            rocks.add((x, y))

    return rocks


def drop_sand(rocks, sand):
    max_y = 0
    for (_, y) in rocks:
        max_y = max(max_y, y)
    pos = START
    while True:
        if pos[1] > max_y:
            return None
        below = pos[0], pos[1] + 1
        below_left = pos[0] - 1, pos[1] + 1
        below_right = pos[0] + 1, pos[1] + 1
        if below not in rocks | sand:
            pos = below
        elif below_left not in rocks | sand:
            pos = below_left
        elif below_right not in rocks | sand:
            pos = below_right
        else:
            return pos


def solve_part1() -> int:
    rocks = load_input()
    sand = set()

    while (landing := drop_sand(rocks, sand)) is not None:
        sand.add(landing)

    return len(sand)


def solve_part2() -> int:
    return 0


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
