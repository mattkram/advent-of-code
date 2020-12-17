import re
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

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
    memory = {}
    and_mask = 0
    or_mask = 0
    for instruction in instructions:
        type_ = instruction["type"]
        value = instruction["value"]
        if type_ == "mask":
            mask = str(value)
            and_mask = int(mask.replace("X", "1"), 2)
            or_mask = int(mask.replace("X", "0"), 2)
        elif type_ == "mem":
            masked_value = int(value) & and_mask | or_mask
            memory[instruction["index"]] = masked_value

    return sum(memory.values())


TEST_INPUTS = [
    (
        """
        mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
        mem[8] = 11
        mem[7] = 101
        mem[8] = 0
        """,
        165,
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
