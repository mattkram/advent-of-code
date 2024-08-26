import re
from collections import deque
from pathlib import Path
from typing import List

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List[List[str]]

TOKEN_PATTERN = re.compile(r"(\d+|[\+\-\*/\(\)])")


def parse(input_str: str) -> ParsedInput:
    """Parse input into a list of tokens."""
    return [TOKEN_PATTERN.findall(line) for line in input_str.splitlines()]


def eval_tokens(input_tokens: List[str]) -> int:
    tokens = deque(input_tokens)

    result = 0
    operator = "+"
    value = None

    while tokens:
        token = tokens.popleft()
        if token == "(":
            # Evaluate expression in parentheses
            parens_tokens = []
            level = 1
            while True:
                token = tokens.popleft()
                if token == "(":
                    level += 1
                elif token == ")":
                    level -= 1

                if level > 0:
                    parens_tokens.append(token)
                else:
                    break
            value = eval_tokens(parens_tokens)
        elif token in "+-*/":
            operator = token
        else:
            value = int(token)

        if operator and value is not None:
            if operator == "+":
                result += value
            elif operator == "-":
                result -= value
            elif operator == "*":
                result *= value
            elif operator == "/":
                result //= value
            else:
                raise ValueError
            operator = ""
            value = None

    return result


def calculate(lines: ParsedInput) -> int:
    return sum(eval_tokens(tokens) for tokens in lines)


TEST_INPUTS = [
    ("1 + 2 * 3 + 4 * 5 + 6", 71),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 26),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
