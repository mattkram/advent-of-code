from collections import Counter

import pytest


INPUT = "245182-790572"


def calculate(input_str: str) -> bool:
    return list(input_str) == sorted(input_str) and 2 in Counter(input_str).values()


@pytest.mark.parametrize(
    "input_str,expected",
    [("112233", True), ("123444", False), ("111122", True)],
)
def test_compare_results(input_str: str, expected: bool) -> None:
    assert calculate(input_str) == expected


def test_compare_final_answer() -> None:
    assert main() == 710


def main() -> int:
    start, end = [int(s) for s in INPUT.split("-")]
    answer = 0
    for value in range(start, end + 1):
        answer += int(calculate(str(value)))
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    exit(main())
