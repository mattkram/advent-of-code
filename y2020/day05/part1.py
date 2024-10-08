from pathlib import Path

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"


def get_val(string: str, keys: str) -> int:
    return sum(keys.index(v) * 2**n for n, v in enumerate(reversed(string)))


def calculate(input_str: str) -> int:
    seats = [line.strip() for line in input_str.split()]
    seat_nums = []
    for seat in seats:
        row = get_val(seat[:7], "FB")
        col = get_val(seat[7:], "LR")
        seat_num = 8 * row + col
        seat_nums.append(seat_num)
    return max(seat_nums)


TEST_INPUTS = [
    ("FBFBBFFRLR", 357),
    ("BFFFBBFRRR", 567),
    ("FFFBBBFRRR", 119),
    ("BBFFBBFRLL", 820),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(fp.read())


if __name__ == "__main__":
    print(f"The answer is {main()}")
