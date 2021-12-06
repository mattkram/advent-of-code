from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    return [int(s) for s in input_str.split(",")]


def advance(data: Dict[int, int]) -> Dict[int, int]:
    new_data: Dict[int, int] = defaultdict(lambda: 0)
    for age, count in data.items():
        if age == 0:
            new_data[6] += count
            new_data[8] += count
        else:
            new_data[age - 1] += count
    return new_data


def calculate(input_str: str, generations: int) -> int:
    data = parse(input_str)  # noqa: F841

    fish_counts: Dict[int, int] = defaultdict(lambda: 0)
    for fish in data:
        fish_counts[fish] += 1

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
