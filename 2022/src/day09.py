from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).parents[1]

DIRECTION_MAP = {
    "R": (+1, 0),
    "L": (-1, 0),
    "U": (0, +1),
    "D": (0, -1),
}


def simulate(num_knots):
    path = Path("data", "day09.txt")
    moves = []
    with path.open() as fp:
        for line in fp:
            if not line.strip():
                continue
            direction, distance = line.strip().split(" ")
            moves.append((direction, int(distance)))
    knots = [(0, 0) for _ in range(num_knots)]

    visited = set()

    for direction, distance in moves:
        vector = DIRECTION_MAP[direction]
        for _ in range(distance):
            # Move the head knot
            knots[0] = (knots[0][0] + vector[0], knots[0][1] + vector[1])
            for idx, (leader, follower) in enumerate(zip(knots, knots[1:]), start=1):
                delta = (leader[0] - follower[0], leader[1] - follower[1])
                distance = (abs(delta[0]), abs(delta[1]))
                if any(d > 1 for d in distance):
                    knots[idx] = (
                        follower[0] + delta[0] / (distance[0] or 1),
                        follower[1] + delta[1] / (distance[1] or 1),
                    )

            visited.add(knots[-1])

    return len(visited)


def solve_part1() -> int:
    return simulate(num_knots=2)


def solve_part2() -> int:
    return simulate(num_knots=10)


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
