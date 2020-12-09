from pathlib import Path
from typing import List

import pytest


def load_input_lines() -> List[str]:
    """Load the input data, returning a list of lines."""
    input_file = Path(__file__).parent / "input.txt"
    with input_file.open() as ff:
        return ff.read().splitlines()


def string_to_machine(input_str: str) -> List[int]:
    """Convert a CSV string to an integer machine."""
    return [int(s) for s in input_str.split(",")]


def run_machine(machine: List[int]) -> None:
    """Run the integer machine, modifying the list in-place."""
    for i in range(0, len(machine), 4):
        instruction = machine[i]
        if instruction == 99:
            return

        ptr = machine[i + 1 : i + 4]
        if instruction == 1:
            machine[ptr[2]] = machine[ptr[0]] + machine[ptr[1]]
        if instruction == 2:
            machine[ptr[2]] = machine[ptr[0]] * machine[ptr[1]]


def calculate(input_str: str) -> List[int]:
    machine = string_to_machine(input_str)
    run_machine(machine)
    return machine


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "1,9,10,3,2,3,11,0,99,30,40,50",
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        ),
        ("1,0,0,0,99", [2, 0, 0, 0, 99]),
        ("2,3,0,3,99", [2, 3, 0, 6, 99]),
        ("2,4,4,5,99,0", [2, 4, 4, 5, 99, 9801]),
        ("1,1,1,4,99,5,6,0,99", [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_compare_results(input_str: str, expected: List[int]) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 2_890_696


def main() -> int:
    lines = load_input_lines()
    machine = string_to_machine(lines[0])
    machine[1:3] = 12, 2
    run_machine(machine)
    result = machine[0]
    print(f"The answer is: {result}")
    return result


if __name__ == "__main__":
    exit(main())
