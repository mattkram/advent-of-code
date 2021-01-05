from collections import deque
from itertools import product
from pathlib import Path
from typing import Dict
from typing import List
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
        try:
            token = tokens.popleft()
        except IndexError:
            return False
        return token == rule

    for sub_rule in rule:
        # While we test the sub-rule, the recursive calls will ultimatately popleft() each
        # match, so we need to work with a copy and then update the overall one if we match
        tokens_cpy = tokens.copy()
        if all(is_valid(tokens_cpy, rules, rule_ind=i) for i in sub_rule):
            while len(tokens) > len(tokens_cpy):
                tokens.popleft()
            if rule_ind == 0 and tokens:
                return False  # Leftover characters
            return True
    return False


def calculate(data: ParsedInput) -> int:
    rules, messages = data
    matches = 0
    for message in messages:
        for num_8, num_11 in product(range(1, 6), range(1, 6)):
            rules[8] = [[42] * num_8]
            rules[11] = [[42] * num_11 + [31] * num_11]
            if is_valid(message, rules):
                matches += 1
                break
    return matches


TEST_INPUTS = [
    (
        """
        0: 8 11
        1: "a"
        2: 1 24 | 14 4
        3: 5 14 | 16 1
        4: 1 1
        5: 1 14 | 15 1
        6: 14 14 | 1 14
        7: 14 5 | 1 21
        8: 42
        9: 14 27 | 1 26
        10: 23 14 | 28 1
        11: 42 31
        12: 24 14 | 19 1
        13: 14 3 | 1 12
        14: "b"
        15: 1 | 14
        16: 15 1 | 14 14
        17: 14 2 | 1 7
        18: 15 15
        19: 14 1 | 14 14
        20: 14 14 | 1 15
        21: 14 1 | 1 14
        22: 14 14
        23: 25 1 | 22 14
        24: 14 1
        25: 1 1 | 1 14
        26: 14 22 | 1 20
        27: 1 6 | 14 18
        28: 16 1
        31: 14 17 | 1 13
        42: 9 14 | 10 1

        abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
        bbabbbbaabaabba
        babbbbaabbbbbabbbbbbaabaaabaaa
        aaabbbbbbaaaabaababaabababbabaaabbababababaaa
        bbbbbbbaaaabbbbaaabbabaaa
        bbbababbbbaaaaaaaabbababaaababaabab
        ababaaaaaabaaab
        ababaaaaabbbaba
        baabbaaaabbaaaababbaababb
        abbbbabbbbaaaababbbbbbaaaababb
        aaaaabbaabaaaaababaa
        aaaabbaaaabbaaa
        aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
        babaaabbbaaabaababbaabababaaab
        aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
        """,
        12,
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
