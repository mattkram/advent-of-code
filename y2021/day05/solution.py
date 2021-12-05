from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


class Point(NamedTuple):
    x: int
    y: int


def parse(input_str: str) -> List[Tuple[Point, Point]]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]

    points = []
    for line in lines:
        pt_1_str, pt_2_str = line.split("->")
        x_1, y_1 = pt_1_str.split(",")
        x_2, y_2 = pt_2_str.split(",")
        pt_1 = Point(int(x_1), int(y_1))
        pt_2 = Point(int(x_2), int(y_2))
        points.append((pt_1, pt_2))
    return points


def calculate(input_str: str, consider_diagonals: bool = False) -> int:
    point_pairs = parse(input_str)  # noqa: F841

    counts: Dict[Point, int] = defaultdict(lambda: 0)
    for pt_1, pt_2 in point_pairs:
        dx = pt_2.x - pt_1.x
        dy = pt_2.y - pt_1.y
        if pt_2.x == pt_1.x:
            for y in range(min(pt_1.y, pt_2.y), max(pt_1.y, pt_2.y) + 1):
                counts[Point(pt_1.x, y)] += 1
        elif pt_2.y == pt_1.y:
            for x in range(min(pt_1.x, pt_2.x), max(pt_1.x, pt_2.x) + 1):
                counts[Point(x, pt_1.y)] += 1
        elif consider_diagonals:
            dx_sgn = dx // abs(dx)
            dy_sgn = dy // abs(dy)
            x_range = range(pt_1.x, pt_2.x + dx_sgn, dx_sgn)
            y_range = range(pt_1.y, pt_2.y + dy_sgn, dy_sgn)
            for x, y in zip(x_range, y_range):
                counts[Point(x, y)] += 1

    return sum(1 for count in counts.values() if count >= 2)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(
            f"The answer to part 1 is {calculate(input_str, consider_diagonals=False)}"
        )
        print(
            f"The answer to part 2 is {calculate(input_str, consider_diagonals=True)}"
        )


if __name__ == "__main__":
    main()
