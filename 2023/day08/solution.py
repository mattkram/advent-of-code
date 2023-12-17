import itertools
import re
from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str, part: int) -> list:
    lines = input_str.splitlines()
    pattern = lines[0]

    result = {}
    for line in lines[2:]:
        if m := re.match(r"(\w+) = \((\w+), (\w+)\)", line):
            result[m.group(1)] = (m.group(2), m.group(3))
        else:
            raise ValueError(f"Could not parse line {line}")

    return pattern, result


def calculate(input_str: str, part: int = 1) -> int:
    pattern, mapping = parse(input_str, part)

    node = "AAA"
    for num_steps, direction in enumerate(itertools.cycle(pattern), start=1):
        left, right = mapping[node]

        if direction == "L":
            node = left
        else:
            node = right

        if node == "ZZZ":
            return num_steps


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str, part=1)}")
        print(f"The answer to part 2 is {calculate(input_str, part=2)}")


if __name__ == "__main__":
    main()
