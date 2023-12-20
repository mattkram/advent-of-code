import itertools
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


def count_possibilities(pattern, counts):
    # Get the index of each "?" in the pattern
    unknowns = [i for i, v in enumerate(pattern) if v == "?"]

    # The total number of damaged expected ("#") in the pattern
    total = sum(counts)

    # The number of spaces to fill with a #
    num_known = sum(v == "#" for v in pattern)
    num_to_add = total - num_known

    # Iterate through all the combinations where we can substitute # for ?
    num_possibilities = 0
    for sub_ind in itertools.combinations(unknowns, num_to_add):
        tmp_pattern = list(pattern)
        for i in sub_ind:
            tmp_pattern[i] = "#"
        possible_pattern = "".join(tmp_pattern).replace("?", ".")

        # Extract all instances of one or more # in a row
        segments = DAMAGED_PATTERN.findall(possible_pattern)

        # Check that the lengths are equal to the target, and if so add that as a possibility
        # This is a silly optimization that cut ~15% off the speed by exiting early instead
        # of constructing a tuple
        for s, c in itertools.zip_longest(segments, counts):
            if len(s) != c:
                break
        else:
            num_possibilities += 1

    return num_possibilities


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)

    result = 0
    for pattern, counts in data:
        result += count_possibilities(pattern, counts)
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
