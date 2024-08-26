import functools
import re
from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"

DAMAGED_PATTERN = re.compile(r"#+")


def parse(input_str: str) -> list[tuple[str, tuple[int, ...]]]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    result = []
    for line in lines:
        pattern, known_str = line.split()
        known = tuple(int(i) for i in known_str.split(","))
        result.append((pattern, known))
    return result


@functools.cache
def count_possibilities(pattern: str, counts: tuple[int, ...]) -> int:
    if pattern == "":
        if counts == tuple() or counts == (0,):
            # We've exhausted all damaged parts or options, and we're not expecting more
            return 1
        else:
            # We're expecting more, but there are no more
            return 0

    first = pattern[0]
    rest = pattern[1:]
    if first == "#":
        if (not counts) or counts[0] == 0:
            return 0
        if len(pattern) < counts[0]:
            return 0
        if "." in pattern[: counts[0]]:
            # The word isn't long enough
            return 0
        # Claim all of them. Add a leading zero to ensure we handle the next dot.
        return count_possibilities(pattern[counts[0] :], (0,) + counts[1:])
    elif first == ".":
        if counts and counts[0] == 0:
            # The dot is a word separator, so remove the zero so we are onto the next word
            return count_possibilities(rest, counts[1:])
        else:
            # Just move to the rest of the word
            return count_possibilities(rest, counts)
    elif first == "?":  # Could be plain else
        return count_possibilities("#" + rest, counts) + count_possibilities(
            "." + rest, counts
        )
    else:
        raise ValueError("Shouldn't get here")


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)

    result = 0
    for pattern, counts in data:
        result += count_possibilities(pattern, counts)
    return result


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)
    result = 0
    for pattern, counts in data:
        pattern = "?".join([pattern] * 5)
        counts *= 5
        result += count_possibilities(pattern, counts)

    return result


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
