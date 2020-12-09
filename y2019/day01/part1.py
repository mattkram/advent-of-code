from pathlib import Path
from typing import List

import pytest


def load_input_lines() -> List[str]:
    """Load the input data, returning a list of lines."""
    input_file = Path(__file__).parent / "input.txt"
    with input_file.open() as ff:
        return ff.read().splitlines()


def lines_to_masses(input_str: str) -> List[int]:
    """Load the input data, returning a list of payload masses."""
    return [int(s) for s in input_str.splitlines()]


def get_required_fuel(mass: int) -> int:
    """Calculate the mass of fuel required to carry another mass."""
    return mass // 3 - 2


def calculate(input_str: str) -> int:
    return get_required_fuel(int(input_str))


@pytest.mark.parametrize(
    "input_str,expected",
    [("12", 2), ("14", 2), ("1969", 654), ("100756", 33583)],
)
def test_compare_results(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 3_426_455


def main() -> int:
    """Get the total required fuel for all modules, not including
    the mass of the fuel required to carry the fuel."""
    lines = load_input_lines()
    total_fuel = sum(calculate(line) for line in lines)
    print(f"Total required fuel for Part 1 is {total_fuel}")
    return total_fuel


if __name__ == "__main__":
    exit(main())
