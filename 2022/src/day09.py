from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).parents[1]

DIRECTION_MAP = {
    "R": (+1, 0),
    "L": (-1, 0),
    "U": (0, +1),
    "D": (0, -1),
}


def parse_data(lines: list[str]) -> list[list[int]]:
    data = []
    for line in lines:
        data.append([int(c) for c in line])
    return data


def solve_part1() -> int:
    path = Path("data", "day09.txt")
    moves = []
    with path.open() as fp:
        for line in fp:
            if not line.strip():
                continue
            direction, distance = line.strip().split(" ")
            moves.append((direction, int(distance)))

    head_pos = (0, 0)
    tail_pos = (0, 0)
    visited = set()

    for direction, distance in moves:
        vector = DIRECTION_MAP[direction]
        for _ in range(distance):
            head_pos = (head_pos[0] + vector[0], head_pos[1] + vector[1])
            delta = (head_pos[0] - tail_pos[0], head_pos[1] - tail_pos[1])
            distance = (abs(delta[0]), abs(delta[1]))
            if any(d > 1 for d in distance):
                tail_pos = (
                    tail_pos[0] + delta[0] / (distance[0] or 1),
                    tail_pos[1] + delta[1] / (distance[1] or 1),
                )

            visited.add(tail_pos)

    return len(visited)


def solve_part2() -> int:
    return 0


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
