from collections import deque
from itertools import product
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

RulesDict = Dict[int, Union[str, List[List[int]]]]
ParsedInput = Tuple[RulesDict, List[str]]


def parse(input_str: str) -> ParsedInput:
    rules_str, messages_str = input_str.split("\n\n")
    rules: RulesDict = {}
    for rule_str in rules_str.strip().splitlines():
        key_str, _, rest = rule_str.partition(": ")
        key = int(key_str)

        if '"' in rest:
            rules[key] = str(rest.strip().replace('"', ""))
        else:
            nested_rules = []
            for s in rest.split("|"):
                nested_rules.append([int(i) for i in s.split()])
            rules[key] = nested_rules

    messages = [line.strip() for line in messages_str.strip().splitlines()]
    return rules, messages


def is_valid(msg: Union[str, deque], rules: RulesDict, rule_ind: int = 0) -> bool:
    rule = rules[rule_ind]

    tokens = deque(msg) if isinstance(msg, str) else msg

    if isinstance(rule, str):
        token = tokens.popleft()
        return token == rule

    for sub_rule in rule:
        tokens_cpy = tokens.copy()
        if all(is_valid(tokens_cpy, rules, rule_ind=i) for i in sub_rule):
            while len(tokens) > len(tokens_cpy):
                tokens.popleft()
            if rule_ind == 0 and tokens:
                return False  # Leftover characters
            return True
    return False


def get_combinations(rules: RulesDict, rule_ind: int = 0) -> Set[str]:

    rule = rules[rule_ind]

    if isinstance(rule, str):
        return {rule}  # Only one combination

    combinations = set()
    for sub_rule in rules[rule_ind]:
        combos = [get_combinations(rules, i) for i in sub_rule]  # type: ignore
        for c in product(*combos):
            combinations.add("".join(c))
    return combinations


def calculate(data: ParsedInput) -> int:
    rules, messages = data
    combinations = get_combinations(rules)
    return sum(msg in combinations for msg in messages)


TEST_INPUTS = [
    (
        """
        0: 4 1 5
        1: 2 3 | 3 2
        2: 4 4 | 5 5
        3: 4 5 | 5 4
        4: "a"
        5: "b"

        ababbb
        """,
        1,
    ),
    (
        """
        0: 4 1 5
        1: 2 3 | 3 2
        2: 4 4 | 5 5
        3: 4 5 | 5 4
        4: "a"
        5: "b"

        ababbb
        bababa
        abbbab
        aaabbb
        aaaabbb
        """,
        2,
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
