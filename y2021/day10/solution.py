from pathlib import Path
from typing import Dict
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"

CHAR_MAP: Dict[str, str] = {"[": "]", "(": ")", "<": ">", "{": "}"}


def parse(input_str: str) -> List[str]:
    return [s.strip() for s in input_str.split() if s.strip()]


class Stack:
    def __init__(self) -> None:
        self._stack: List[str] = []

    def push(self, item: str) -> None:
        self._stack.append(item)

    def pop(self) -> str:
        return self._stack.pop(-1)

    def __str__(self) -> str:
        return str(self._stack)

    def __len__(self) -> int:
        return len(self._stack)

    def __bool__(self) -> bool:
        return bool(self._stack)


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    score_map = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    score = 0
    for line in data:
        stack = Stack()
        for char in line:
            if char in CHAR_MAP.keys():
                stack.push(char)
            else:
                try:
                    top = stack.pop()
                except IndexError:
                    score += score_map[char]
                else:
                    if char == CHAR_MAP[top]:
                        continue
                score += score_map[char]
    return score


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    score_map = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    scores = []
    for line in data:
        stack = Stack()
        for char in line:
            if char in CHAR_MAP.keys():
                stack.push(char)
            else:
                try:
                    top = stack.pop()
                except IndexError:
                    break  # skip this line

                if char != CHAR_MAP[top]:
                    break  # skip this line

        else:
            score = 0
            while stack:
                top = stack.pop()
                score = 5 * score + score_map[CHAR_MAP[top]]
            scores.append(score)

    return sorted(scores)[len(scores) // 2]


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
