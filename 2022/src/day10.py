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
    history = []
    cycle = 1
    cumulative_signal_strength = 0
    with path.open() as fp:
        for line in fp:
            match line.split():
                case ["noop"]:
                    column = (cycle - 1) % 40
                    if register - 1 <= column <= register + 1:
                        history.append("#")
                    else:
                        history.append(".")
                    cycle += 1
                    if (cycle - 20) % 40 == 0:
                        cumulative_signal_strength += register * cycle
                case ["addx", s]:
                    value = int(s)

                    column = (cycle - 1) % 40
                    if register - 1 <= column <= register + 1:
                        history.append("#")
                    else:
                        history.append(".")
                    cycle += 1
                    if (cycle - 20) % 40 == 0:
                        cumulative_signal_strength += register * cycle

                    column = (cycle - 1) % 40
                    if register - 1 <= column <= register + 1:
                        history.append("#")
                    else:
                        history.append(".")
                    register += value
                    cycle += 1
                    if (cycle - 20) % 40 == 0:
                        cumulative_signal_strength += register * cycle

    return cumulative_signal_strength, history


def solve_part1() -> int:
    return simulate()[0]


def solve_part2() -> None:
    history = simulate()[1]
    for row in range(len(history) // 40):
        line = "".join(history[40 * row : 40 * (row + 1)])
        line = line.replace(".", "\N{MEDIUM BLACK CIRCLE}").replace(
            "#", "\N{LARGE YELLOW CIRCLE}"
        )
        print(line)


if __name__ == "__main__":
    print(f"The answer to part 1 is: {solve_part1()}")
    solve_part2()
