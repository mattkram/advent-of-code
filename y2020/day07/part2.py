import re
from pathlib import Path
from typing import Dict

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Dict[str, Dict[str, int]]

PATTERN = re.compile(r"(.*) bag.* contain (\d+ .* bag)+")
SUB_PATTERN = re.compile(r"(\d+) (.*?) bag")


def parse(input_str: str) -> ParsedInput:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    bag_dict = {}
    for line in lines:
        if m := PATTERN.match(line):
            owner, rest = m.groups()
            children = SUB_PATTERN.findall(rest)
            bag_dict[owner] = {child: int(num) for num, child in children}
    return bag_dict


def num_contained(sub_dict: Dict[str, int], bag_dict: ParsedInput) -> int:
    total = 0
    for key, num_bags in sub_dict.items():
        num_sub_bags = num_contained(bag_dict.get(key, {}), bag_dict)
        total += num_bags * (num_sub_bags + 1)
    return total


def calculate(bag_dict: ParsedInput) -> int:
    return num_contained(bag_dict["shiny gold"], bag_dict)


TEST_INPUTS = [
    (
        """
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
        dotted black bags contain no other bags.
        """,
        32,
    ),
    (
        """
        shiny gold bags contain 2 dark red bags.
        dark red bags contain 2 dark orange bags.
        dark orange bags contain 2 dark yellow bags.
        dark yellow bags contain 2 dark green bags.
        dark green bags contain 2 dark blue bags.
        dark blue bags contain 2 dark violet bags.
        dark violet bags contain no other bags.
        """,
        126,
    ),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
