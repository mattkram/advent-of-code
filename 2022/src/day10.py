from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).parents[1]

DIRECTION_MAP = {
    "R": (+1, 0),
    "L": (-1, 0),
    "U": (0, +1),
    "D": (0, -1),
}


def simulate():
    path = Path("data", "day10.txt")
    register = 1
    history = [register]
    cycle = 1
    cumulative_signal_strength = 0
    with path.open() as fp:
        for line in fp:
            match line.split():
                case ["noop"]:
                    history.append(register)
                    cycle += 1
                    if (cycle - 20) % 40 == 0:
                        cumulative_signal_strength += register * cycle
                case ["addx", s]:
                    value = int(s)

                    history.append(register)
                    cycle += 1
                    if (cycle - 20) % 40 == 0:
                        cumulative_signal_strength += register * cycle

                    history.append(register)
                    register += value
                    cycle += 1
                    if (cycle - 20) % 40 == 0:
                        cumulative_signal_strength += register * cycle

    return cumulative_signal_strength


def solve_part1() -> int:
    return simulate()


def solve_part2() -> int:
    return simulate()


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    print(f"The answer to part 2 is: {solve_part2()}")
