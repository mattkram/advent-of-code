from pathlib import Path

import pytest

from .solution import calculate_part1
from .solution import calculate_part2
from .solution import Node
from .solution import parse
from .solution import reduce

TEST_INPUT = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
        # (REAL_INPUT, 50),
    ],
)
def test_reduce(input_str: str, expected: int) -> None:
    data = parse(input_str)
    reduce(data)
    assert str(data) == expected


def test_full_reduce() -> None:
    data = parse("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    while reduce(data):
        ...
    assert str(data) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            """
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            """,
            "[[[[1,1],[2,2]],[3,3]],[4,4]]",
        ),
        (
            """
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            [5,5]
            """,
            "[[[[3,0],[5,3]],[4,4]],[5,5]]",
        ),
        (
            """
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            [5,5]
            [6,6]
            """,
            "[[[[5,0],[7,4]],[5,5]],[6,6]]",
        ),
        (
            """
            [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
            [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
            [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
            [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
            [7,[5,[[3,8],[1,4]]]]
            [[2,[2,2]],[8,[8,1]]]
            [2,9]
            [1,[[[9,3],9],[[9,0],[0,7]]]]
            [[[5,[7,4]],7],1]
            [[[[4,2],2],6],[8,7]]
            """,
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        ),
    ],
)
def test_list_of_sums(input_str: str, expected: str) -> None:
    lines = [line.strip() for line in input_str.splitlines() if line.strip()]
    node = parse(lines.pop(0))
    while reduce(node):
        ...
    while lines:
        old_node = node
        node = Node(left=old_node, right=parse(lines.pop(0)))
        while reduce(node):
            ...
    assert str(node) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_magnitude(input_str: str, expected: int) -> None:
    data = parse(input_str)
    assert data.magnitude == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 4140),
        (REAL_INPUT, 4417),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (TEST_INPUT, 3993),
        (REAL_INPUT, 4796),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
