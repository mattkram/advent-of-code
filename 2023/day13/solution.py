from __future__ import annotations

from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> list[list[str]]:
    patterns = []
    for section in input_str.strip().split("\n\n"):
        lines = [s.strip() for s in section.splitlines() if s.strip()]
        patterns.append(lines)
    return patterns


def find_horizontal_reflection(pattern: list[str], skip_index=None) -> int | None:
    """Find the reflection point horizontally, if it exists, otherwise return None."""

    reflect_indexes = [i for i, p in enumerate(pattern[:-1]) if pattern[i + 1] == p]

    for reflect_index in reflect_indexes:
        left = pattern[reflect_index::-1]
        right = pattern[reflect_index + 1 :]
        if all(a == b for a, b in zip(left, right)):
            index = reflect_index + 1
            if skip_index is None:
                return index
            else:
                if index != skip_index:
                    return index
    return None


def transpose(pattern: list[str]) -> list[str]:
    result = []
    for col in zip(*pattern):
        result.append("".join(col))

    return result


def find_reflection(pattern, skip_index=None):
    if (
        score := find_horizontal_reflection(transpose(pattern), skip_index=skip_index)
    ) is not None:
        return score
    if (
        score := find_horizontal_reflection(pattern, skip_index=skip_index)
    ) is not None:
        return score * 100
    raise ValueError("Shouldn't get here")


def calculate_part1(input_str: str) -> int:
    patterns = parse(input_str)

    result = 0
    for pattern in patterns:
        result += find_reflection(pattern)

    return result


def find_reflection_with_smudge(pattern, original_score):
    num_rows = len(pattern)
    num_cols = len(pattern[0])

    if original_score % 100 == 0:
        # It was horizontal
        original_index_horz = original_score // 100
        original_index_vert = None
    else:
        original_index_horz = None
        original_index_vert = original_score

    for row in range(num_rows):
        for col in range(num_cols):
            # In this first part, we make a new copy of the pattern, but swap a single entry
            tmp_pattern = [list(r) for r in pattern]
            tmp_pattern[row][col] = "#" if tmp_pattern[row][col] == "." else "."
            new_pattern = ["".join(r) for r in tmp_pattern]

            if (
                score := find_horizontal_reflection(
                    transpose(new_pattern), skip_index=original_index_vert
                )
            ) is not None:
                return score
            if (
                score := find_horizontal_reflection(
                    new_pattern, skip_index=original_index_horz
                )
            ) is not None:
                return score * 100
    raise ValueError("Shouldn't get here")


def calculate_part2(input_str: str) -> int:
    patterns = parse(input_str)

    result = 0
    for pattern in patterns:
        original_score = find_reflection(pattern)
        result += find_reflection_with_smudge(pattern, original_score)

    return result


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
