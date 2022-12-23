from __future__ import annotations

import string
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]

INFINITY = 1_000_000
Coord = tuple[int, int]

ELEVATIONS = {c: i for i, c in enumerate(string.ascii_lowercase)} | {"S": 0, "E": 25}


def load_input() -> tuple[dict[Coord, str], Coord, Coord]:
    path = Path("data", "day12.txt")
    board = {}
    with path.open() as fp:
        lines = [line.strip() for line in fp if line.strip()]
    start = (0, 0)
    end = (0, 0)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            board[i, j] = char
            match char:
                case "S":
                    start = (i, j)
                case "E":
                    end = (i, j)

    return board, start, end


def solve_part1() -> int:
    """We implement Dijkstra's algorithm to find the shortest path."""
    squares, source, end = load_input()

    dist = {}
    Q = set()
    for v in squares:
        dist[v] = INFINITY
        Q.add(v)

    dist[source] = 0

    while Q:
        u = min(Q, key=lambda v: dist[v])
        Q.remove(u)
        el_u = ELEVATIONS[squares[u]]
        for offset in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
            # v is the potential neighboring node
            v = (u[0] + offset[0], u[1] + offset[1])
            if v not in Q:
                # Not in graph
                continue
            el_v = ELEVATIONS[squares[v]]
            if el_v - el_u > 1:
                # Ineligible neighbor (too high of a step)
                continue
            # The potential distance from u->v is 1
            dist[v] = min(dist[v], dist[u] + 1)

    return dist[end]


def solve_part2() -> int:
    return 0


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
