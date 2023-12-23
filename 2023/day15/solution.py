from __future__ import annotations

import re
from pathlib import Path


INPUTS_FILE = Path(__file__).parent / "input.txt"
STEP_PATTERN = re.compile(r"(\w+)([-=])(\d+)?")


def parse(input_str: str) -> list[str]:
    return input_str.strip().split(",")


def HASH(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256

    return value


def calculate_part1(input_str: str) -> int:
    sequence = parse(input_str)
    return sum(HASH(step) for step in sequence)


def calculate_part2(input_str: str) -> int:
    sequence = parse(input_str)
    boxes = [[] for _ in range(256)]
    for step in sequence:
        if m := STEP_PATTERN.match(step):
            label = m.group(1)
            operation = m.group(2)
            focal_length = m.group(3)
        else:
            raise ValueError("Bad instruction")

        box = boxes[HASH(label)]

        if operation == "-":
            box[:] = [(lbl, fl) for lbl, fl in box if lbl != label]
        elif operation == "=":
            lens = (label, int(focal_length))
            if existing := [i for i, (lbl, fl) in enumerate(box) if lbl == label]:
                box[existing[0]] = lens
            else:
                box.append(lens)
        else:
            raise ValueError("Bad operation")

    focusing_power = 0
    for i, box in enumerate(boxes, start=1):
        for j, (label, focal_length) in enumerate(box, start=1):
            focusing_power += i * j * focal_length

    return focusing_power


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
