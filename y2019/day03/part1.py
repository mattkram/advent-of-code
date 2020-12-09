from pathlib import Path
from typing import List
from typing import Tuple

import pytest


def load_input_lines() -> List[str]:
    """Load the input data, returning a list of lines."""
    input_file = Path(__file__).parent / "input.txt"
    with input_file.open() as ff:
        return ff.read().splitlines()


def route_to_pts(route_string: str) -> List[Tuple[int, int]]:
    """Convert a route string to a list of points."""
    instructions = route_string.split(",")

    points = [(0, 0)]
    for instruction in instructions:
        direction = instruction[0]
        num_steps = int(instruction[1:])
        for value in range(num_steps):
            new_pt = list(points[-1])
            if direction == "R":
                new_pt[0] += 1
            if direction == "L":
                new_pt[0] -= 1
            if direction == "U":
                new_pt[1] += 1
            if direction == "D":
                new_pt[1] -= 1
            points.append((new_pt[0], new_pt[1]))
    return points


def get_min_distance_manhattan(route_strings: List[str]) -> int:
    """Get the minimum distance using Manhattan distance."""
    route_1_pts = route_to_pts(route_strings[0])
    route_2_pts = route_to_pts(route_strings[1])

    intersections = set(route_1_pts).intersection(set(route_2_pts))
    distance = [abs(x) + abs(y) for x, y in intersections]
    return min(d for d in distance if d > 0)


def calculate(input_str: str) -> int:
    route_strings = input_str.splitlines()
    return get_min_distance_manhattan(route_strings)


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("R8,U5,L5,D3\nU7,R6,D4,L4", 6),
        (
            "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83",
            159,
        ),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            135,
        ),
    ],
)
def test_compare_results(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 316


def main() -> int:
    lines = load_input_lines()
    answer = get_min_distance_manhattan(lines)
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
