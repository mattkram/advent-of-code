from collections import deque
from pathlib import Path
from typing import Deque
from typing import Dict

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = Dict[int, Deque[int]]


def parse(input_str: str) -> ParsedInput:
    players: ParsedInput = {}
    for section in input_str.strip().split("\n\n"):
        player_str, *cards = section.splitlines()
        player_num = int(player_str.replace("Player", "").replace(":", ""))
        players[player_num] = deque(int(card) for card in cards)
    return players


def calculate(decks: ParsedInput) -> int:
    while all(decks.values()):
        value_1 = decks[1].popleft()
        value_2 = decks[2].popleft()
        if value_1 > value_2:
            decks[1].extend([value_1, value_2])
        else:
            decks[2].extend([value_2, value_1])

    for deck in decks.values():
        if deck:
            return sum(i * v for i, v in enumerate(reversed(deck), start=1))

    raise ValueError("Cannot find an answer")


TEST_INPUTS = [
    (
        """
        Player 1:
        9
        2
        6
        3
        1

        Player 2:
        5
        8
        4
        7
        10
        """,
        306,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
