import itertools
import math
import re
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ClassDict = Dict[str, Set[int]]
ParsedInput = Tuple[ClassDict, List[int], List[List[int]]]

CLASS_PATTERN = re.compile(r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)")


def parse(input_str: str) -> ParsedInput:
    classes, yours, nearby = [s.strip() for s in input_str.split("\n\n") if s.strip()]

    class_dict: ClassDict = {}
    for c in classes.splitlines():
        if (m := CLASS_PATTERN.match(c.strip())) :
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
    my_ticket = get_my_ticket(data)
    return math.prod(v for rule, v in my_ticket.items() if rule.startswith("departure"))


def get_my_ticket(data: ParsedInput) -> Dict[str, int]:
    rules, mine, nearby = data

    all_rules = set(itertools.chain.from_iterable(rules.values()))

    valid_nearby = [ticket for ticket in nearby if all(v in all_rules for v in ticket)]

    # Begin with a set of all items a rule might apply to
    rules_possible = {rule: set(range(len(mine))) for rule in rules}

    # We will construct a mapping of each rule to its column
    rules_map = {}

    while rules_possible:
        # Go through all tickets, eliminating columns from the rules
        # that aren't satisfied by its values
        for ticket in valid_nearby:
            for i, value in enumerate(ticket):
                for rule, values_allowed in rules.items():
                    if value not in values_allowed:
                        try:
                            rules_possible[rule].remove(i)
                        except KeyError:
                            pass

        # Once a rule has only one index allowed, add it to the
        # rule map and remove from rules_possible
        for rule, possibilities in dict(rules_possible).items():
            if len(possibilities) == 1:
                (rules_map[rule],) = possibilities
                rules_possible.pop(rule)

        # Now remove all mapped rule indices from the existing possibilities
        for rule, possibilities in rules_possible.items():
            for value in rules_map.values():
                try:
                    possibilities.remove(value)
                except KeyError:
                    pass

    # Use the index map to construct my ticket
    my_ticket_map = {rule: mine[i] for rule, i in rules_map.items()}
    return my_ticket_map


TEST_INPUTS = [
    (
        """
        class: 0-1 or 4-19
        row: 0-5 or 8-19
        seat: 0-13 or 16-19

        your ticket:
        11,12,13

        nearby tickets:
        3,9,18
        15,1,5
        5,14,9
        """,
        {"class": 12, "row": 11, "seat": 13},
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert get_my_ticket(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
