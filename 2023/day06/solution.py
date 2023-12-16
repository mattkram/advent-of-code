import math
from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str, concat: bool) -> None:
    times = []
    distances = []
    for line in input_str.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("Time:"):
            times.extend(int(t) for t in line.split()[1:])

        elif line.startswith("Distance:"):
            distances.extend(int(d) for d in line.split()[1:])

    if not concat:
        races = list(zip(times, distances))
    else:
        races = [
            (
                int("".join(str(t) for t in times)),
                int("".join(str(d) for d in distances)),
            )
        ]
    return races


def count_ways_to_win(time, distance):
    # Iterate until we break the distance record.
    # Then, since this is some type of symmetric sequence, we can just calculate the rest with math.
    t = 0
    while t <= time:
        if (time - t) * t > distance:
            break
        t += 1

    return time - (t * 2) + 1


def calculate(input_str: str, concat: bool = False) -> int:
    races = parse(input_str, concat=concat)

    ways_to_win = []
    for time, distance in races:
        w = count_ways_to_win(time, distance)
        ways_to_win.append(w)

    return math.prod(ways_to_win)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str)}")
        print(f"The answer to part 2 is {calculate(input_str, concat=True)}")


if __name__ == "__main__":
    main()
