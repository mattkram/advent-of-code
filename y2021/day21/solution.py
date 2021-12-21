import re
from functools import lru_cache
from pathlib import Path
from typing import Dict
from typing import Generator
from typing import Tuple

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


dup_map = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


@lru_cache(maxsize=None)
def get_num_wins(
    position_1: int,
    position_2: int,
    score_1: int = 0,
    score_2: int = 0,
    player: int = None,
    roll_total: int = None,
) -> Tuple[int, int]:

    if roll_total is not None:
        if player == 1:
            position_1 = (position_1 + roll_total - 1) % 10 + 1
            score_1 += position_1
        else:
            position_2 = (position_2 + roll_total - 1) % 10 + 1
            score_2 += position_2

    if score_1 >= 21:
        return 1, 0
    elif score_2 >= 21:
        return 0, 1

    if player is None or player == 2:
        player = 1
    else:
        player = 2

    tot_player_1_wins = 0
    tot_player_2_wins = 0
    for tot, dup in dup_map.items():
        player_1_wins, player_2_wins = get_num_wins(
            position_1, position_2, score_1, score_2, player, tot
        )
        tot_player_1_wins += dup * player_1_wins
        tot_player_2_wins += dup * player_2_wins

    return tot_player_1_wins, tot_player_2_wins


def calculate_part2(input_str: str) -> int:
    positions = parse(input_str)
    num_wins = get_num_wins(positions[1], positions[2])
    return max(num_wins)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
