import itertools
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ClassDict = Dict[str, Set[int]]
ParsedInput = Tuple[ClassDict, List[int], List[List[int]]]

CLASS_PATTERN = re.compile(r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)")


def parse(input_str: str) -> ParsedInput:
    classes, yours, nearby = [s.strip() for s in input_str.split("\n\n") if s.strip()]

    class_dict: ClassDict = {}
    for c in classes.splitlines():
        if m := CLASS_PATTERN.match(c.strip()):
            key, *ind_str = m.groups()
            ind = [int(i) for i in ind_str]
            class_dict[key] = set(range(ind[0], ind[1] + 1)) | set(
                range(ind[2], ind[3] + 1)
            )

    my_list = [int(i) for i in yours.splitlines()[1].split(",")]

    nearby_list: List[List[int]] = []
    for n in nearby.splitlines()[1:]:
        nearby_list.append([int(i) for i in n.split(",")])

    return class_dict, my_list, nearby_list


def calculate(data: ParsedInput) -> int:
    classes, _, nearby = data

    all_rules = set(itertools.chain.from_iterable(classes.values()))
    num_invalid = sum(v for n in nearby for v in n if v not in all_rules)

    return num_invalid


TEST_INPUTS = [
    (
        """
        class: 1-3 or 5-7
        row: 6-11 or 33-44
        seat: 13-40 or 45-50

        your ticket:
        7,1,14

        nearby tickets:
        7,3,47
        40,4,50
        55,2,20
        38,6,12
        """,
        71,
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
