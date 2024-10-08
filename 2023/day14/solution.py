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
                # Place this rock after the last non-empty space
                place_row = non_empty_ind[-1] + 1
            else:
                # Otherwise, stop at top of mirror
                place_row = 0

            mirror[i][j] = Item.EMPTY
            mirror[place_row][j] = Item.ROUND_ROCK
            pass

    return mirror


def count_weight(mirror: list[list[Item]]) -> int:
    num_rows = len(mirror)
    result = 0

    for i, row in enumerate(mirror):
        num_rocks = sum(item == Item.ROUND_ROCK for item in row)
        result += num_rocks * (num_rows - i)
    return result


def calculate_part1(input_str: str) -> int:
    mirror = parse(input_str)
    mirror = tilt_up(mirror)
    return count_weight(mirror)


def rotate(mirror: list[list[Item]]) -> list[list[Item]]:
    """Rotate 90 degrees clockwise."""
    num_rows = len(mirror)
    num_cols = len(mirror[0])
    result = [[0 for _ in range(num_rows)] for _ in range(num_cols)]
    for i, row in enumerate(mirror):
        for j, item in enumerate(row):
            new_col = num_rows - i - 1
            new_row = j
            result[new_row][new_col] = item
    return result


def calculate_hash(mirror):
    string = "".join(item.value for row in mirror for item in row)
    return hash(string)


def calculate_part2(input_str: str) -> int:
    mirror = parse(input_str)
    num_cycles = 1000000000

    hash_history = []
    weight_map = {}
    first_occurrence = -1
    cycle_length = -1
    for cycle in range(num_cycles):
        for _ in range(4):
            mirror = tilt_up(mirror)
            mirror = rotate(mirror)
        h = calculate_hash(mirror)
        if h in hash_history:
            first_occurrence = hash_history.index(h)
            cycle_length = cycle - first_occurrence
            break

        weight_map[h] = count_weight(mirror)
        hash_history.append(h)

    index = (num_cycles - first_occurrence - 1) % cycle_length + first_occurrence

    final_hash = hash_history[index]
    return weight_map[final_hash]


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
