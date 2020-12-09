import re
from collections import Counter
from pathlib import Path

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"
PASSWORD_PATTERN = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def calculate(input_str: str) -> int:
    lines = [s.strip() for s in input_str.split("\n") if s.strip()]
    num_valid = 0
    for line in lines:
        if m := PASSWORD_PATTERN.match(line.strip()):
            min_num, max_num, letter, password = m.groups()
            letter_counts = Counter(password)
            if int(min_num) <= letter_counts[letter] <= int(max_num):
                num_valid += 1
    return num_valid


TEST_INPUTS = [
    (
        """
        1-3 a: abcde
        1-3 b: cdefg
        2-9 c: ccccccccc
        """,
        2,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(fp.read())


if __name__ == "__main__":
    print(f"The answer is {main()}")
