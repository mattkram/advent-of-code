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


"""
* If current state of decks has been seen before in another round, then game over
    * Previous rounds from other games are not considered

* Draw cards
    * The value of each card just drawn must be <= number of cards remaining in their deck
        * If this is so, then a new game is played
    * Otherwise the winner of the round is the player with the higher-value card

"""
GAME_NUM = 0


def play_game(decks: ParsedInput) -> int:
    global GAME_NUM
    game_num = GAME_NUM + 1
    GAME_NUM += 1

    print(f"\n=== Game {game_num} ===\n")
    round_num = 1

    # history = set()
    MAX_ROUND = 17  # 00000000000000000
    while all(decks.values()) and round_num <= MAX_ROUND:
        #        t = tuple(decks[1])
        #        if t in history:
        #            return 1
        #         print(t)
        #         print(history)
        #        history.add(t)

        print(f"-- Round {round_num} (Game {game_num}) --")
        for i in [1, 2]:
            print(f"Player {i}'s deck: {', '.join(str(d) for d in decks[i])}")

        value = {i: deck.popleft() for i, deck in decks.items()}
        for i in decks.keys():
            print(f"Player {i} plays: {value[i]}")

        if all(value[i] <= len(decks[i]) for i in decks.keys()):
            print("Playing a sub-game to determine the winner...")
            new_decks = {i: deque(list(deck)[: value[i]]) for i, deck in decks.items()}
            winner = play_game(new_decks)
            loser = 1 if winner == 2 else 1
            print(f"...anyway, back to game {game_num}.")
        elif value[1] > value[2]:
            winner = 1
            loser = 2
        else:
            winner = 2
            loser = 1
        print(f"Player {winner} wins round {round_num} of game {game_num}!")
        decks[winner].extend([value[winner], value[loser]])
        print()
        round_num += 1

    for player_num, deck in decks.items():
        if deck:
            print(f"The winner of game {game_num} is player {player_num}!")
            print()
            return player_num

    raise ValueError("Cannot find an answer")


def calculate(decks: ParsedInput) -> int:
    play_game(decks)
    print("== Post-game results ==")
    for i, deck in decks.items():
        print(f"Player {i}'s deck:", ", ".join(str(d) for d in deck))
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
        291,
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
