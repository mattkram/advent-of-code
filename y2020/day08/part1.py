from pathlib import Path
from typing import List, Tuple

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[Tuple[str, int]]


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    instructions = []
    for line in lines:
        op, val = line.split()
        instructions.append((op, int(val)))
    return instructions


def calculate(instructions: ParsedInput) -> int:
    accumulator = 0
    pointer = 0

    used_instructions = set()

    while True:
        op, val = instructions[pointer]
        if pointer in used_instructions:
            return accumulator

        used_instructions.add(pointer)

        if op == "nop":
            pointer += 1
        elif op == "acc":
            pointer += 1
            accumulator += val
        elif op == "jmp":
            pointer += val
        else:
            raise ValueError(f"Unknown opcode: {op}")

    raise ValueError("Cannot find an answer")


TEST_INPUTS = [
    (
        """
        nop +0
        acc +1
        jmp +4
        acc +3
        jmp -3
        acc -99
        acc +1
        jmp -4
        acc +6
        """,
        5,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
