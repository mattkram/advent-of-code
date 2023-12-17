from collections import Counter
from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


class Card:
    _value_map = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, name: str):
        self.value = int(self._value_map.get(name, name))

    def __gt__(self, other: "Card") -> bool:
        return self.value > other.value

    def __eq__(self, other: "Card") -> bool:
        return self.value == other.value


class Hand:
    def __init__(self, line: str):
        cards, bid = line.split()
        self.cards_str = cards

        self._bid = int(bid)
        self._cards = tuple(Card(s) for s in cards)
        self.type = None

    @property
    def value(self) -> int:
        """Assign an integer value based on the hand type."""
        c = Counter(c.value for c in self._cards)
        counts = dict(c)
        s = tuple(sorted(counts.values(), reverse=True))
        if s == (5,):
            self.type = "Five of a kind!"
            return 6
        elif s == (4, 1):
            self.type = "Four of a kind"
            return 5
        elif s == (3, 2):
            self.type = "Full house"
            return 4
        elif s == (3, 1, 1):
            self.type = "Three of a kind"
            return 3
        elif s == (2, 2, 1):
            self.type = "Two pair"
            return 2
        elif s == (2, 1, 1, 1):
            self.type = "One pair"
            return 1
        elif s == (1, 1, 1, 1, 1):
            self.type = "High card"
            return 0
        raise ValueError(f"Unknown hand: {self.cards_str}")

    def __gt__(self, other: "Hand") -> bool:
        if self.value > other.value:
            return True
        elif self.value < other.value:
            return False
        else:
            return self._cards > other._cards


def parse(input_str: str, part: int) -> list[Hand]:
    return [Hand(line) for line in input_str.splitlines()]


def calculate(input_str: str, part: int = 1) -> int:
    hands = parse(input_str, part=part)
    result = 0
    for i, hand in enumerate(sorted(hands), start=1):
        print(f"Rank {i}: {hand.cards_str}, {hand.type}")
        result += i * hand._bid
    return result


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str, part=1)}")
        print(f"The answer to part 2 is {calculate(input_str, part=2)}")


if __name__ == "__main__":
    main()
