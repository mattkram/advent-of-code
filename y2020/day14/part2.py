import re
from itertools import product
from pathlib import Path
from typing import Dict, List, Union

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[Dict[str, Union[str, int]]]

MASK_PATTERN = re.compile(r"mask = (\w+)")
MEM_PATTERN = re.compile(r"mem\[(\d+)\] = (\d+)")


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    instructions: ParsedInput = []
    for line in lines:
        if m := MASK_PATTERN.match(line):
            instructions.append(
                {
                    "type": "mask",
                    "value": m.group(1),
                }
            )
        elif m := MEM_PATTERN.match(line):
            instructions.append(
                {
                    "type": "mem",
                    "index": int(m.group(1)),
                    "value": int(m.group(2)),
                }
            )
        else:
            raise ValueError
    return instructions


def calculate(instructions: ParsedInput) -> int:
    memory: Dict[int, int] = {}
    mask = 0
    for instruction in instructions:
        type_ = instruction["type"]
        value = instruction["value"]
        if type_ == "mask":
            x_ind = [i for i, s in enumerate(reversed(str(value))) if s == "X"]
            mask = int(str(value).replace("X", "0"), 2)
        elif type_ == "mem":
            address = int(instruction["index"])
            for it in product([0, 1], repeat=len(x_ind)):
                new_address = address | mask
                for i, n in zip(it, x_ind):
                    if i == 0:
                        new_address &= ~(1 << n)
                    else:
                        new_address |= 1 << n

                    memory[new_address] = int(value)

    return sum(memory.values())


TEST_INPUTS = [
    (
        """
        mask = 000000000000000000000000000000X1001X
        mem[42] = 100
        mask = 00000000000000000000000000000000X0XX
        mem[26] = 1
        """,
        208,
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
