import itertools
import math
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple


INPUTS_FILE = Path(__file__).parent / "input.txt"

Data = List[Tuple[int, int]]


class Node:
    left: Optional["Node"]
    right: Optional["Node"]
    value: Optional[int]
    parent: Optional["Node"]

    def __init__(
        self,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
        value: Optional[int] = None,
        parent: Optional["Node"] = None,
    ):
        self.left = left
        if left is not None:
            left.parent = self
        self.right = right
        if right is not None:
            right.parent = self
        self.value = value
        self.parent = parent

    @classmethod
    def from_list(cls, data: List) -> "Node":
        if isinstance(data, int):
            return Node(value=data)
        left, right = data
        node = Node(left=Node.from_list(left), right=Node.from_list(right))
        return node

    @property
    def depth(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    def __repr__(self) -> str:
        if self.value is not None:
            return str(self.value)
        return f"[{self.left},{self.right}]"

    @property
    def magnitude(self) -> int:
        if self.value is not None:
            return self.value
        assert self.left is not None
        assert self.right is not None
        return 3 * self.left.magnitude + 2 * self.right.magnitude


def flatten_tree(node: Node) -> List[Node]:
    if node.value is not None:
        return [node]

    assert node.left is not None
    assert node.right is not None
    result = []
    result.extend(flatten_tree(node.left))
    result.extend(flatten_tree(node.right))
    return result


def parse(input_str: str) -> Node:
    return Node.from_list(eval(input_str))


def reduce(data: Node) -> bool:
    flat_data = flatten_tree(data)
    # Look for nodes to explode
    for i, node in enumerate(flat_data):
        if node.parent is not None and node.parent.depth >= 4:
            parent = node.parent
            if (left_ind := i - 1) >= 0:
                flat_data[left_ind].value += node.parent.left.value  # type: ignore
            if (right_ind := i + 2) <= len(flat_data) - 1:
                flat_data[right_ind].value += node.parent.right.value  # type: ignore
            parent.left = None
            parent.right = None
            parent.value = 0
            return True
    # Look for nodes to split
    for node in flat_data:
        if node.value is not None and node.value > 9:
            node.left = Node(value=math.floor(node.value / 2), parent=node)
            node.right = Node(value=math.ceil(node.value / 2), parent=node)
            node.value = None
            return True

    return False


def calculate_part1(input_str: str) -> int:
    lines = [line.strip() for line in input_str.splitlines() if line.strip()]
    node = parse(lines.pop(0))
    while reduce(node):
        ...
    while lines:
        old_node = node
        node = Node(left=old_node, right=parse(lines.pop(0)))
        while reduce(node):
            ...
    return node.magnitude


def calculate_part2(input_str: str) -> int:
    lines = [line.strip() for line in input_str.splitlines() if line.strip()]
    result = 0
    for left, right in itertools.permutations(lines, r=2):
        node = Node(left=parse(left), right=parse(right))
        while reduce(node):
            ...
        result = max(result, node.magnitude)
    return result


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
