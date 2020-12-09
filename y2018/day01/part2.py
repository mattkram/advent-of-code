from itertools import cycle
from typing import List

import pytest

from .part1 import load_input_lines


def calculate(input_str: List[str]) -> int:
    value = 0
    seen = set()
    seen.add(value)
    for freq_change in cycle(input_str):
        value += int(freq_change)
        if value in seen:
            return value
        seen.add(value)

    raise ValueError("Value never encountered twice.")


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("+1, -1", 0),
        ("+3, +3, +4, -2, -4", 10),
        ("-6, +3, +8, +5, -6", 5),
        ("+7, +7, -2, -7, -4", 14),
    ],
)
def test_compare_results(input_str: str, expected: int) -> None:
    assert calculate(input_str.split(", ")) == expected


def test_compare_final_answer() -> None:
    assert main() == 66932


def main() -> int:
    """Get the total required fuel for all modules, not including
    the mass of the fuel required to carry the fuel."""
    lines = load_input_lines()
    answer = calculate(lines)
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
