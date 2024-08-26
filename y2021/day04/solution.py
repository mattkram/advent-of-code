from pathlib import Path
from typing import List, Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


Board = List[List[int]]


def parse(input_str: str) -> Tuple[List[int], List[Board]]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    draws = [int(s) for s in lines.pop(0).split(",")]
    num_boards = len(lines) // 5

    int_lines = [[int(s) for s in line.split()] for line in lines]

    boards = []
    for i in range(num_boards):
        boards.append(int_lines[5 * i : 5 * (i + 1)])

    return draws, boards


def winning_board(board: Board, history: List[int]) -> bool:
    for row in board:
        if all(item in history for item in row):
            return True
    for col in zip(*board):
        if all(item in history for item in col):
            return True
    return False


def sum_remaining(board: Board, history: List[int]) -> int:
    return sum(item for row in board for item in row if item not in history)


def calculate_part1(input_str: str) -> int:
    draws, boards = parse(input_str)  # noqa: F841

    for i in range(1, len(draws)):
        history = draws[:i]

        for board in boards:
            if winning_board(board, history):
                return sum_remaining(board, history) * history[-1]

    raise ValueError("Cannot find an answer")


def calculate_part2(input_str: str) -> int:
    draws, boards = parse(input_str)  # noqa: F841

    for i in range(1, len(draws)):
        history = draws[:i]

        if len(boards) == 1 and winning_board(boards[0], history):
            return sum_remaining(boards[0], history) * history[-1]

        boards = [board for board in boards if not winning_board(board, history)]

    raise ValueError("Cannot find an answer")


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
