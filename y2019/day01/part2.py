import pytest

from .part1 import get_required_fuel, load_input_lines


def get_required_fuel_recursive(mass: int) -> int:
    """Calculate the total fuel required to carry a given mass,
    recursively including the fuel required to carry that fuel."""
    fuel_mass = get_required_fuel(mass)
    if fuel_mass <= 0:
        return 0
    return fuel_mass + get_required_fuel_recursive(fuel_mass)


def calculate(input_str: str) -> int:
    return get_required_fuel_recursive(int(input_str))


@pytest.mark.parametrize(
    "input_str,expected", [("14", 2), ("1969", 966), ("100756", 50346)]
)
def test_compare_results(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 5_136_807


def main() -> int:
    """Get the total required fuel for all modules, including
    the mass of the fuel required to carry the fuel."""
    lines = load_input_lines()
    total_fuel = sum(calculate(line) for line in lines)
    print(f"Total required fuel for Part 2 is {total_fuel}")
    return total_fuel


if __name__ == "__main__":
    exit(main())
