from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Dict[str, List[str]]:
    data = defaultdict(lambda: [])
    for line in input_str.strip().splitlines():
        source, target = line.strip().split("-")
        data[source].append(target)
        if source != "start" and target != "end":
            data[target].append(source)
    return dict(data)


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841

    num_routes = 0

    def count_routes(
        source: str = "start", prev_route: Optional[List[str]] = None
    ) -> None:
        nonlocal num_routes
        prev_route = list(prev_route or [])

        if source.islower() and source in prev_route:
            return

        if source == "end":
            num_routes += 1
            return

        for target in data.get(source, []):
            count_routes(target, prev_route + [source])

    count_routes("start")
    return num_routes


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    raise ValueError("Cannot find an answer")


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
