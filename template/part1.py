from pathlib import Path

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"


def calculate(input_str: str) -> int:
    values = [int(s) for s in input_str.split()]  # noqa: F841
    # TODO: Put the solution here
    raise ValueError("Cannot find an answer")


TEST_INPUTS = [
    (
        """
        1721
        979
        366
        299
        675
        1456
        """,
        514579,
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
