from __future__ import annotations

from itertools import zip_longest
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]

Packet = list[list[int] | int]


def load_input() -> list[tuple[Packet, Packet]]:
    path = Path("data", "day13.txt")
    instructions = []
    with path.open() as fp:
        line_pairs = fp.read().strip().split("\n\n")
        for pair in line_pairs:
            instructions.append(tuple(eval(s) for s in pair.split("\n")))

    return instructions


class Result(Exception):
    def __init__(self, *args, result: bool, level: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = result
        self.level = level

    def __str__(self) -> str:
        if self.result:
            return (
                f"{(self.level+1) * '  '}- Left side is smaller, "
                "so inputs are in the right order"
            )
        else:
            return (
                f"{(self.level + 1) * '  '}- Right side is smaller, "
                "so inputs are not in the right order"
            )


def compare(left: Packet, right: Packet, level: int = 0) -> None:
    """Return true if ordered, i.e. right > left."""
    print(f"{level * '  '}- Compare {left} vs {right}")

    if isinstance(left, int) and isinstance(right, int):
        if left != right:
            raise Result(result=left < right, level=level)
    elif isinstance(left, list) and isinstance(right, list):
        for item_l, item_r in zip_longest(left, right):
            if item_l is None:
                raise Result(result=True, level=level)
            elif item_r is None:
                raise Result(result=False, level=level)
            else:
                compare(item_l, item_r, level + 1)
    else:
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        compare(left, right, level + 1)


def solve_part1() -> int:
    instructions = load_input()
    num_ordered = 0
    for i, (first, second) in enumerate(instructions, start=1):
        print(f"== Pair {i} ==")
        try:
            compare(first, second)
        except Result as e:
            print(e)
            if e.result:
                num_ordered += i

    return num_ordered


def solve_part2() -> int:
    return 0


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
