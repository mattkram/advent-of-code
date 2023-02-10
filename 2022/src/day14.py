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


def drop_sand(rocks, sand, max_y, include_floor=False):
    # TODO: This is very slow. We actually should only need to track the
    #       rocks and top layer of sand in each column, I think,
    #       which would potentially speed up the contact lookup significantly
    pos = START
    while True:
        if pos[1] > max_y:
            return None
        below = pos[0], pos[1] + 1
        below_left = pos[0] - 1, pos[1] + 1
        below_right = pos[0] + 1, pos[1] + 1
        if include_floor and below[1] == max_y:
            return pos
        taken = rocks | sand
        if below not in taken:
            pos = below
        elif below_left not in taken:
            pos = below_left
        elif below_right not in taken:
            pos = below_right
        else:
            return pos


def solve_part1() -> int:
    rocks = load_input()
    sand = set()

    max_y = 0
    for _, y in rocks:
        max_y = max(max_y, y)

    while (landing := drop_sand(rocks, sand, max_y)) is not None:
        sand.add(landing)

    return len(sand)


def solve_part2() -> int:
    rocks = load_input()
    sand = set()

    max_y = 0
    for _, y in rocks:
        max_y = max(max_y, y)

    # for x in range(200, 800):
    #     rocks.add((x, max_y + 2))

    it = 0
    while True:
        landing = drop_sand(rocks, sand, max_y + 2, include_floor=True)
        if landing is None:
            break
        if it % 100 == 0:
            print(landing)
        sand.add(landing)
        if landing == START:
            break
        it += 1

    return len(sand)


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
