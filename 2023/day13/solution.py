from __future__ import annotations

from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> list[list[str]]:
    patterns = []
    for section in input_str.strip().split("\n\n"):
        lines = [s.strip() for s in section.splitlines() if s.strip()]
        patterns.append(lines)
    return patterns


def find_horizontal_reflection(pattern: list[str]) -> int | None:
    """Find the reflection point horizontally, if it exists, otherwise return None."""

    reflect_indexes = [i for i, p in enumerate(pattern[:-1]) if pattern[i + 1] == p]

    for reflect_index in reflect_indexes:
        left = pattern[reflect_index::-1]
        right = pattern[reflect_index + 1 :]
        if all(a == b for a, b in zip(left, right)):
            return reflect_index + 1
    return None


def transpose(pattern: list[str]) -> list[str]:
    result = []
    for col in zip(*pattern):
        result.append("".join(col))

    return result


def find_reflection(pattern):
    if (score := find_horizontal_reflection(transpose(pattern))) is not None:
        return score
    if (score := find_horizontal_reflection(pattern)) is not None:
        return score * 100
    return 0


def calculate_part1(input_str: str) -> int:
    patterns = parse(input_str)

    result = 0
    for pattern in patterns:
        result += find_reflection(pattern)

    return result


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    raise ValueError("Cannot find an answer")


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
