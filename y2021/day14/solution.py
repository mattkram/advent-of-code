from collections import Counter
from functools import cache  # type: ignore
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


def calculate(input_str: str, num_steps: int = 10) -> int:
    template, rules = parse(input_str)  # noqa: F841

    @cache
    def get_counts(left: str, right: str, level: int = 0) -> Counter:
        inner_counter = Counter()  # type: ignore

        if level == num_steps:
            inner_counter[left] += 1
            return inner_counter

        combo = left + right
        if combo in rules:
            inner_counter.update(get_counts(left, rules[combo], level=level + 1))
            inner_counter.update(get_counts(rules[combo], right, level=level + 1))

        return inner_counter

    counter = Counter({template[-1]: 1})
    for left, right in zip(template, template[1:]):
        counter.update(get_counts(left, right))

    return max(counter.values()) - min(counter.values())


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str, num_steps=10)}")
        print(f"The answer to part 2 is {calculate(input_str, num_steps=40)}")


if __name__ == "__main__":
    main()
