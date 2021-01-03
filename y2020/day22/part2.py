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


def play_game(decks: ParsedInput) -> int:
    history = set()
    while all(decks.values()):
        t = tuple(tuple(deck) for deck in decks.values())
        if t in history:
            return 1
        history.add(t)

        value = {i: deck.popleft() for i, deck in decks.items()}

        if all(value[i] <= len(deck) for i, deck in decks.items()):
            new_decks = {i: deque(list(deck)[: value[i]]) for i, deck in decks.items()}
            winner = play_game(new_decks)
        elif value[1] > value[2]:
            winner = 1
        else:
            winner = 2
        loser = 1 if winner == 2 else 2
        decks[winner].extend([value[winner], value[loser]])

    for player_num, deck in decks.items():
        if deck:
            return player_num

    raise ValueError("Cannot find an answer")


def calculate(decks: ParsedInput) -> int:
    winner = play_game(decks)
    return sum(i * v for i, v in enumerate(reversed(decks[winner]), start=1))


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
        291,
    ),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
