import re
from pathlib import Path
from typing import Dict
from typing import Generator


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Dict[int, int]:
    starting_positions = {}
    for line in input_str.strip().splitlines():
        if m := re.match(r"Player (\d) starting position: (\d+)", line.strip()):
            starting_positions[int(m.group(1))] = int(m.group(2))
        else:
            raise ValueError(f"Could not parse {line.strip()}")
    return starting_positions


def calculate_part1(input_str: str) -> int:
    positions = parse(input_str)
    limit = 1000
    scores = {1: 0, 2: 0}

    num_rolls = 1

    def _roll() -> Generator[int, None, None]:
        nonlocal num_rolls
        roll_value = 1
        while True:
            yield roll_value
            roll_value = roll_value % 100 + 1
            num_rolls += 1

    dice_roll = _roll()

    player = 1
    while all(v < limit for v in scores.values()):
        for _ in range(3):
            positions[player] += next(dice_roll)

        positions[player] = (positions[player] - 1) % 10 + 1
        scores[player] += positions[player]

        # Switch to other player
        player = 1 if player == 2 else 2

    return min(scores.values()) * num_rolls


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
