from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

INFINITY = 1_000_000_000

INPUTS_FILE = Path(__file__).parent / "input.txt"

Graph = Dict[Tuple[int, int], "Node"]


class Node:

    NODE_COUNT = 0

    def __init__(self, energy: int):
        self.energy = energy
        self.dist = INFINITY
        self.neighbors: Set[Node] = set()
        self._id: int = Node.NODE_COUNT
        Node.NODE_COUNT += 1
        self.prev: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node(energy={self.energy}, dist={self.dist})"

    def __hash__(self) -> int:
        return self._id


def multiply_boards(ints: List[List[int]], multiplier: int) -> List[List[int]]:
    new_ints = []

    for row_repeat in range(multiplier):
        for row in ints:
            new_row = []
            for col_repeat in range(multiplier):
                for value in row:
                    new_value = ((value + col_repeat + row_repeat) - 1) % 9 + 1
                    new_row.append(new_value)
            new_ints.append(new_row)
    return new_ints


def parse(input_str: str, multiplier: int = 1) -> Graph:
    lines = [str(s.strip()) for s in input_str.splitlines() if s.strip()]
    ints = [[int(s) for s in line] for line in lines]
    ints = multiply_boards(ints, multiplier)

    nodes: Graph = {}
    for i, line in enumerate(ints):
        for j, value in enumerate(line):
            node = Node(energy=value)
            nodes[i, j] = node

    for (row, col), node in nodes.items():
        for row_offset, col_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            try:
                target = nodes[row + row_offset, col + col_offset]
            except KeyError:
                continue

            node.neighbors.add(target)

    nodes[0, 0].dist = 0
    return nodes


def get_min_energy_path(graph: Graph) -> int:
    max_row, max_col = max(graph.keys())
    nodes = set(graph.values())
    while nodes:
        min_dist = INFINITY
        min_dist_node, *_ = nodes
        for node in nodes:
            if node.dist < min_dist:
                min_dist_node = node
                min_dist = node.dist

        nodes.remove(min_dist_node)

        if min_dist_node == graph[max_row, max_col]:
            break

        for neighbor in min_dist_node.neighbors:
            if neighbor not in nodes:
                continue

            alt = min_dist + neighbor.energy
            if alt < neighbor.dist:
                neighbor.dist = alt
                neighbor.prev = min_dist_node

    node = graph[max_row, max_col]
    total = 0
    while node.prev is not None:
        total += node.energy
        node = node.prev
    return total


def calculate_part1(input_str: str) -> int:
    graph = parse(input_str)  # noqa: F841
    return get_min_energy_path(graph)


def calculate_part2(input_str: str) -> int:
    graph = parse(input_str, multiplier=5)  # noqa: F841
    return get_min_energy_path(graph)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        # print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
