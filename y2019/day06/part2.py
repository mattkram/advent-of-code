from typing import List

import pytest

from .part1 import OrbitalMap, load_input_lines


def calculate(input_lines: List[str]) -> int:
    m = OrbitalMap(input_lines)
    return m.get_num_transfers("YOU", "SAN")


@pytest.mark.parametrize(
    "input_lines,expected",
    [
        (
            [
                "COM)B",
                "B)C",
                "C)D",
                "D)E",
                "E)F",
                "B)G",
                "G)H",
                "D)I",
                "E)J",
                "J)K",
                "K)L",
                "K)YOU",
                "I)SAN",
            ],
            4,
        )
    ],
)
def test_compare_results(input_lines: List[str], expected: bool) -> None:
    assert calculate(input_lines) == expected


def test_compare_final_answer() -> None:
    assert main() == 442


def main() -> int:
    lines = load_input_lines()
    answer = calculate(lines)
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    main()
