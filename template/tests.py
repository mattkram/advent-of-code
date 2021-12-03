import pytest

from .solution import calculate_part1
from .solution import calculate_part2


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            """
            some_input
            abc
            """,
            10,
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
            some_input
            abc
            """,
            15,
        )
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
