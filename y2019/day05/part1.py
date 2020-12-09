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


def run_machine(machine: List[int], input_value: int = 1) -> List[int]:
    """Run the integer machine, modifying the list in-place."""
    outputs = []

    # Map the instruction code to number of parameters expected
    num_param_dict = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3,
        99: 0,
    }

    ptr = 0
    while True:
        mode_int, instruction = divmod(machine[ptr], 100)
        num_param = num_param_dict[instruction]

        params = machine[ptr + 1 : ptr + num_param + 1]

        # Extract values, either directly or by reference
        values = []
        for param in params:
            mode_int, mode = divmod(mode_int, 10)
            if mode == 1:
                # Directly
                values.append(param)
            else:
                # Reference
                values.append(machine[param])

        # Execute the instruction
        if instruction == 1:
            machine[params[-1]] = values[0] + values[1]
        elif instruction == 2:
            machine[params[-1]] = values[0] * values[1]
        elif instruction == 3:
            machine[params[-1]] = input_value
        elif instruction == 4:
            outputs.append(values[0])
        elif instruction == 5:
            if values[0] != 0:
                ptr = values[1]
                continue
        elif instruction == 6:
            if values[0] == 0:
                ptr = values[1]
                continue
        elif instruction == 7:
            machine[params[-1]] = int(values[0] < values[1])
        elif instruction == 8:
            machine[params[-1]] = int(values[0] == values[1])
        elif instruction == 99:
            break

        ptr += num_param + 1

    return outputs


def calculate(input_str: str) -> List[int]:
    machine = string_to_machine(input_str)
    run_machine(machine)
    return machine


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("1002,4,3,4,33", [1002, 4, 3, 4, 99]),
    ],
)
def test_compare_results(input_str: str, expected: List[int]) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 6761139


def main() -> int:
    lines = load_input_lines()
    machine = string_to_machine(lines[0])
    outputs = run_machine(machine, input_value=1)
    print(outputs)
    answer = outputs[-1]
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
