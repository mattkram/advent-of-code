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


def eval_parens(input_tokens: List[str]) -> List[str]:
    tokens = deque(input_tokens)

    out_tokens = []
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
            token = str(eval_tokens(parens_tokens))
        out_tokens.append(token)
    return out_tokens


def eval_additions(input_tokens: List[str]) -> List[str]:
    tokens = deque(input_tokens)

    output_tokens: List[str] = []
    while tokens:
        token = tokens.popleft()
        if token == "+":
            token = str(int(output_tokens.pop()) + int(tokens.popleft()))
        elif token == "-":
            token = str(int(output_tokens.pop()) - int(tokens.popleft()))
        output_tokens.append(token)
    return output_tokens


def eval_products(input_tokens: List[str]) -> List[str]:
    tokens = deque(input_tokens)

    output_tokens: List[str] = []
    while tokens:
        token = tokens.popleft()
        if token == "*":
            token = str(int(output_tokens.pop()) * int(tokens.popleft()))
        elif token == "/":
            token = str(int(output_tokens.pop()) / int(tokens.popleft()))
        output_tokens.append(token)
    return output_tokens


def eval_tokens(input_tokens: List[str]) -> int:
    tokens = list(input_tokens)
    tokens = eval_parens(tokens)
    tokens = eval_additions(tokens)
    tokens = eval_products(tokens)
    return int(tokens[0])


def calculate(lines: ParsedInput) -> int:
    return sum(eval_tokens(tokens) for tokens in lines)


TEST_INPUTS = [
    ("1 + 2 * 3 + 4 * 5 + 6", 231),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 46),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
