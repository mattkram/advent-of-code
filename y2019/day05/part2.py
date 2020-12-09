from .part1 import load_input_lines
from .part1 import run_machine
from .part1 import string_to_machine


def test_compare_final_answer() -> None:
    assert main() == 9217546


def main() -> int:
    lines = load_input_lines()
    machine = string_to_machine(lines[0])
    outputs = run_machine(machine, input_value=5)
    print(outputs)
    answer = outputs[-1]
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
