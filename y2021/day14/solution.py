from collections import Counter
from itertools import zip_longest
from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Tuple[List[str], Dict[str, str]]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    template = [str(c) for c in lines[0]]
    rules = {}
    for line in lines[1:]:
        from_, to = line.split(" -> ")
        rules[from_] = to
    return template, rules


def calculate_part1(input_str: str, num_steps: int = 10) -> int:
    template, rules = parse(input_str)  # noqa: F841

    for _ in range(num_steps):
        new_template = []

        for a, b in zip_longest(template, template[1:]):
            new_template.append(a)
            if b is None:
                break
            try:
                new_template.append(rules[a + b])
            except KeyError:
                pass

        template = new_template
    counter = Counter(template)
    return max(counter.values()) - min(counter.values())


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    raise ValueError("Cannot find an answer")


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
