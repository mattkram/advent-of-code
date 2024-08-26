import pytest

from .solution import calculate_part1, calculate_part2


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            """
            199
            200
            208
            210
            200
            207
            240
            269
            260
            263
            """,
            7,
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
            199
            200
            208
            210
            200
            207
            240
            269
            260
            263
            """,
            5,
        )
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate_part2(input_str) == expected
