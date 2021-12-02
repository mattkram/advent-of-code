import pytest

from .solution import calculate_part1
from .solution import calculate_part2


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            """
            forward 5
            down 5
            forward 8
            up 3
            down 8
            forward 2
            """,
            150,
        )
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate_part1(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            """
            forward 5
            down 5
            forward 8
            up 3
            down 8
            forward 2
            """,
            900,
        )
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
