from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import field
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]


class Monkey:
    id: int
    items: list[int] = field(default_factory=list)
    op: str
    val: str
    div: int
    if_true: int
    if_false: int
    inspection_count: int = 0

    @classmethod
    def from_lines(cls, lines: list[str]) -> Monkey:
        monkey = cls()
        monkey.id = int(re.match(r"Monkey (\d):", lines[0]).group(1))
        items = re.match(r"Starting items: ([\d, ]+)", lines[1]).group(1)
        monkey.items = [int(i) for i in items.split(", ")]

        m = re.match(r"Operation: new = old ([+*]) (\w+)", lines[2])
        monkey.op = m.group(1)
        monkey.val = m.group(2)

        monkey.div = int(re.match(r"Test: divisible by (\d+)", lines[3]).group(1))

        monkey.if_true = int(
            re.match(r"If true: throw to monkey (\d+)", lines[4]).group(1)
        )
        monkey.if_false = int(
            re.match(r"If false: throw to monkey (\d+)", lines[5]).group(1)
        )

        return monkey

    def get_new_worry_level(self, worry_level: int) -> int:
        if self.val == "old":
            val = worry_level
        else:
            val = int(self.val)

        match self.op:
            case "+":
                worry_level += val
                print(f"    Worry level increases by {self.val} to {worry_level}")
            case "*":
                worry_level *= val
                print(f"    Worry level is multiplied by {self.val} to {worry_level}")
            case _:
                raise ValueError(f"Unknown op: {self.op}")
        return worry_level

    def inspect_and_get_throws(self) -> dict[int, list[int]]:
        print(f"Monkey {self.id}")
        result = defaultdict(list)
        for worry_level in self.items:
            print(f"  Monkey inspects an item with a worry level of {worry_level}.")
            worry_level = self.get_new_worry_level(worry_level)
            worry_level //= 3
            print(
                f"    Monkey gets bored with item. Worry level is divided by 3 to {worry_level}."
            )
            if worry_level % self.div == 0:
                print(f"    Current worry level is divisible by {self.div}.")
                who_to = self.if_true
            else:
                print(f"    Current worry level is not divisible by {self.div}.")
                who_to = self.if_false
            print(
                f"    Item with worry level {worry_level} is thrown to monkey {who_to}."
            )
            result[who_to].append(worry_level)
            self.inspection_count += 1
        return dict(result)


def load_input():
    path = Path("data", "day11.txt")
    monkeys = []
    with path.open() as fp:
        lines = [line.strip() for line in fp if line.strip()]
    num_monkeys = len(lines) // 6
    for i in range(num_monkeys):
        monkeys.append(Monkey.from_lines(lines[6 * i : 6 * (i + 1)]))
    return monkeys


def play_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        throws = monkey.inspect_and_get_throws()
        monkey.items.clear()
        for id_, items in throws.items():
            monkeys[id_].items.extend(items)


def solve_part1() -> int:
    monkeys = load_input()
    for _ in range(20):
        play_round(monkeys)
    counts = sorted((m.inspection_count for m in monkeys), reverse=True)
    return counts[0] * counts[1]


def solve_part2() -> int:
    return 0


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
