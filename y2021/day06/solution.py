from collections import Counter
from pathlib import Path
from typing import Generator

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Generator[int, None, None]:
    for s in input_str.split(","):
        yield int(s)


def advance(data: Counter) -> Counter:
    new_data: Counter = Counter()
    for age, count in data.items():
        if age == 0:
            new_data.update({6: count, 8: count})
        else:
            new_data.update({age - 1: count})
    return new_data


def calculate(input_str: str, generations: int) -> int:
    fish_counts = Counter(parse(input_str))
    for i in range(generations):
        fish_counts = advance(fish_counts)
    return sum(fish_counts.values())


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str, generations=80)}")
        print(f"The answer to part 2 is {calculate(input_str, generations=256)}")


if __name__ == "__main__":
    main()
