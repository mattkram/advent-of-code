from typing import List

import pytest

from .part1 import load_input_lines, route_to_pts


def get_min_distance_path_length(route_strings: List[str]) -> int:
    """Return minimum path distance by indexing the route to each intersection."""
    route_1_pts = route_to_pts(route_strings[0])
    route_2_pts = route_to_pts(route_strings[1])

    intersections = set(route_1_pts).intersection(set(route_2_pts))
    distance = [route_1_pts.index(i) + route_2_pts.index(i) for i in intersections]
    return min(d for d in distance if d > 0)


def calculate(input_str: str) -> int:
    route_strings = input_str.splitlines()
    return get_min_distance_path_length(route_strings)


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83",
            610,
        ),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            410,
        ),
    ],
)
def test_compare_results(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 16368


def main() -> int:
    lines = load_input_lines()
    answer = get_min_distance_path_length(lines)
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
