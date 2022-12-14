from __future__ import annotations

from pathlib import Path
from typing import Any


TOTAL_DISK_SPACE = 70_000_000
REQUIRED_DISK_SPACE = 30_000_000


class Node:
    def __init__(self, *, name: str, parent: "Node" | None = None):
        self.name = name
        self.parent = parent

    @property
    def level(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.level + 1


class File(Node):
    def __init__(self, *, size: int, **kwargs: Any):
        super().__init__(**kwargs)
        self.size = size

    def __str__(self) -> str:
        return (
            f"{'  ' * self.level}\N{BULLET} File(name='{self.name}', size={self.size})"
        )


class Directory(Node):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.children: dict[str, Node] = {}

    def add_child(self, node: Node) -> None:
        node.parent = self
        self.children[node.name] = node

    @property
    def size(self) -> int:
        return sum(nd.size for nd in self.children.values())

    def __str__(self) -> str:
        lines = [f"{'  ' * self.level}\N{BULLET} Directory(name='{self.name}')"]
        for child in self.children.values():
            lines.append(str(child))
        return "\n".join(lines)

    def subdir_sizes(self) -> list[int]:
        sizes = [self.size]
        for nd in self.children.values():
            if isinstance(nd, Directory):
                sizes.extend(nd.subdir_sizes())
        return sizes


def build_tree(lines: list[str]) -> Directory:
    root = Directory(name="/")

    cwd = root
    for line in lines:
        match line.split():
            case ["$", "cd", "/"]:
                cwd = root
            case ["$", "cd", ".."]:
                cwd = cwd.parent
            case ["$", "cd", name]:
                cwd = cwd.children[name]
            case ["$", "ls"]:
                pass
            case ["dir", name]:
                d = Directory(name=name)
                cwd.add_child(d)
            case [size, name]:
                f = File(size=int(size), name=name)
                cwd.add_child(f)

    return root


def solve_part1() -> int:
    path = Path("data", "day07.txt")
    with path.open() as fp:
        tree = build_tree(fp.readlines())

    return sum(size for size in tree.subdir_sizes() if size < 100_000)


def solve_part2() -> int:
    path = Path("data", "day07.txt")
    with path.open() as fp:
        tree = build_tree(fp.readlines())

    unused_disk_space = TOTAL_DISK_SPACE - tree.size
    for size in sorted(tree.subdir_sizes()):
        if unused_disk_space + size > REQUIRED_DISK_SPACE:
            return size
    raise ValueError("Never reached a solution")


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
