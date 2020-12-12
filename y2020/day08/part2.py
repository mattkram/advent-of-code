from pathlib import Path
from typing import List
from typing import Tuple

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


class InfiniteLoopError(Exception):
    pass


def run_machine(instructions: ParsedInput) -> int:
    accumulator = 0
    pointer = 0

    used_instructions = set()

    while True:
        try:
            op, val = instructions[pointer]
        except IndexError:
            if pointer <= 0:
                raise
            return accumulator

        if pointer in used_instructions:
            raise InfiniteLoopError(f"Accumulator: {accumulator}")

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


def calculate(instructions: ParsedInput) -> int:
    for i, (op, value) in enumerate(instructions):
        if op == "jmp":
            new_op = "nop"
        elif op == "nop":
            new_op = "jmp"
        else:
            continue

        new_instructions = list(instructions)
        new_instructions[i] = (new_op, value)
        try:
            accumulator = run_machine(new_instructions)
        except InfiniteLoopError:
            continue
        else:
            return accumulator

    raise ValueError("Cannot find a solution")


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
        8,
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
