from collections import Counter

import pytest

INPUT = "245182-790572"


def calculate(input_str: str) -> bool:
    return (
        list(input_str) == sorted(input_str) and max(Counter(input_str).values()) >= 2
    )


@pytest.mark.parametrize(
    "input_str,expected",
    [("111111", True), ("223450", False), ("123789", False)],
)
def test_compare_results(input_str: str, expected: bool) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 1099


def main() -> int:
    start, end = [int(s) for s in INPUT.split("-")]
    answer = 0
    for value in range(start, end + 1):
        answer += int(calculate(str(value)))
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
