import math
from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> None:
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

    races = list(zip(times, distances))
    return races


def count_ways_to_win(time, distance):
    result = 0
    for t in range(time + 1):
        if (time - t) * t > distance:
            result += 1
    return result


def calculate(input_str: str) -> int:
    print()
    races = parse(input_str)

    ways_to_win = []
    for time, distance in races:
        ways_to_win.append(count_ways_to_win(time, distance))

    return math.prod(ways_to_win)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str)}")
        print(f"The answer to part 2 is {calculate(input_str)}")


if __name__ == "__main__":
    main()
