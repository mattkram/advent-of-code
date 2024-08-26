from __future__ import annotations

import string
from heapq import heappop, heappush
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


def get_shortest_distance(squares, source, end) -> int:
    dist = {source: 0}
    Q = []
    remaining = set()
    for v in squares:
        if v != source:
            dist[v] = INFINITY
        heappush(Q, (dist[v], v))
        remaining.add(v)

    # We need to track any items that should get removed from the priority queue
    # since we will change priority throughout
    removed = set()
    while Q:
        try:
            # Pop off removed items until we get one that's not removed
            while (item := heappop(Q)) in removed:
                removed.remove(item)
        except IndexError:
            # We may try to pop the last removed square, so we should break out
            break
        _, u = item
        remaining.remove(u)
        el_u = ELEVATIONS[squares[u]]
        for offset in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
            # v is the potential neighboring node
            v = (u[0] + offset[0], u[1] + offset[1])
            if v not in remaining:
                # Not in graph
                continue
            el_v = ELEVATIONS[squares[v]]
            if el_v - el_u > 1:
                # Ineligible neighbor (too high of a step)
                continue
            # The potential distance from u->v is 1
            alt = dist[u] + 1
            if alt < dist[v]:
                # Mark this specific old entry as removed
                removed.add((dist[v], v))
                dist[v] = alt
                # Add the new one to the priority queue
                heappush(Q, (alt, v))

    return dist[end]


def solve_part1() -> int:
    """We implement Dijkstra's algorithm to find the shortest path."""
    squares, source, end = load_input()
    return get_shortest_distance(squares, source, end)


def solve_part2() -> int:
    squares, _, end = load_input()
    sources = {k for k, v in squares.items() if v in {"a", "S"}}
    return min(get_shortest_distance(squares, source, end) for source in sources)


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
