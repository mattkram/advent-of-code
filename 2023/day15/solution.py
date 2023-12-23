import re
from pathlib import Path


INPUTS_FILE = Path(__file__).parent / "input.txt"


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
        if m := re.match(r"(\w+)-", step):
            label = m.group(1)
            operation = "-"
        elif m := re.match(r"(\w+)=(\d+)", step):
            label = m.group(1)
            operation = "="
            focal_length = int(m.group(2))
        else:
            raise ValueError("Bad instruction")
        h = HASH(label)
        box = boxes[h]

        if operation == "-":
            box[:] = [(lbl, fl) for lbl, fl in box if lbl != label]
        elif operation == "=":
            existing = [i for i, (lbl, fl) in enumerate(box) if lbl == label]
            if existing:
                box[existing[0]] = (label, focal_length)
            else:
                box.append((label, focal_length))
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
