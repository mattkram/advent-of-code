from pathlib import Path
from typing import List

import pytest


def load_input_lines() -> List[str]:
    """Load the input data, returning a list of lines."""
    input_file = Path(__file__).parent / "input.txt"
    with input_file.open() as ff:
        return ff.read().splitlines()


def calculate(input_str: List[str]) -> int:
    value = 0
    for freq_change in input_str:
        value += int(freq_change)
    return value


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("+1, -2, +3, +1", 3),
        ("+1, +1, +1", 3),
        ("+1, +1, -2", 0),
        ("-1, -2, -3", -6),
    ],
)
def test_compare_results(input_str: str, expected: int) -> None:
    assert calculate(input_str.split(", ")) == expected


def test_compare_final_answer() -> None:
    assert main() == 472


def main() -> int:
    """Get the total required fuel for all modules, not including
    the mass of the fuel required to carry the fuel."""
    lines = load_input_lines()
    answer = calculate(lines)
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
