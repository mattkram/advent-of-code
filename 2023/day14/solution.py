from copy import deepcopy
from enum import Enum
from pathlib import Path


INPUTS_FILE = Path(__file__).parent / "input.txt"


class Item(Enum):
    CUBE_ROCK = "#"
    ROUND_ROCK = "O"
    EMPTY = "."


def parse(input_str: str) -> list[list[Item]]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    return [[Item(c) for c in line] for line in lines]


def tilt_up(mirror: list[list[Item]]) -> list[list[Item]]:
    mirror = deepcopy(mirror)

    for i, row in enumerate(mirror[1:], start=1):
        for j, item in enumerate(row):
            if item != Item.ROUND_ROCK:
                continue

            above = [mirror[ii][j] for ii in range(i)]
            non_empty_ind = [ii for ii, aa in enumerate(above) if aa != Item.EMPTY]
            if non_empty_ind:
                # Place this rock there
                place_row = non_empty_ind[-1] + 1
            else:
                place_row = 0

            if place_row == i:
                continue
            mirror[i][j] = Item.EMPTY
            mirror[place_row][j] = Item.ROUND_ROCK
            pass
        print(f"Row {i}")
        print_mirror(mirror)
        # break

    return mirror


def count_weight(mirror: list[list[Item]]) -> int:
    num_rows = len(mirror)
    result = 0

    for i, row in enumerate(mirror):
        num_rocks = sum(item == Item.ROUND_ROCK for item in row)
        result += num_rocks * (num_rows - i)
    return result


def print_mirror(mirror):
    for row in mirror:
        s = "".join(item.value for item in row)
        print(s)
    print()


def calculate_part1(input_str: str) -> int:
    mirror = parse(input_str)

    print()
    print("Initial:")
    print_mirror(mirror)
    mirror = tilt_up(mirror)

    print("Final:")
    print_mirror(mirror)

    return count_weight(mirror)


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
