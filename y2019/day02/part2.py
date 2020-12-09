from typing import List
from typing import Tuple

from .part1 import load_input_lines
from .part1 import run_machine
from .part1 import string_to_machine


def find_machine_noun_and_verb(machine: List[int], target: int) -> Tuple[int, int]:
    for noun in range(100):
        for verb in range(100):
            new_machine = list(machine)
            new_machine[1:3] = noun, verb
            run_machine(new_machine)
            if new_machine[0] == target:
                return (noun, verb)

    raise ValueError("Could not find an appropriate noun, verb pair")


def test_compare_final_answer() -> None:
    assert main() == 8226


def main() -> int:
    target = 19_690_720
    lines = load_input_lines()
    machine = string_to_machine(lines[0])
    noun, verb = find_machine_noun_and_verb(machine, target)
    print(f"The noun is: {noun}, the verb is: {verb}")

    answer = 100 * noun + verb
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
