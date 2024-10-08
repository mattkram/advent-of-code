import itertools
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"

COST_MAP = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

SLOT_MAP = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}


class Pod(NamedTuple):
    char: str
    energy: int = 0

    def __repr__(self) -> str:
        return self.char


Coords = Tuple[int, int]
Board = Dict[Coords, Optional[Pod]]


def parse(input_str: str) -> Board:
    data = [char for char in input_str if char in "ABCD"]

    board: Board = {}
    for i, char in enumerate(data):
        row = i // 4 + 1
        col = 2 * (i % 4 + 1)
        board[row, col] = Pod(char)

    for i in range(11):
        board[0, i] = None

    return board


def print_board(board: Board) -> None:
    print(f"Total Energy: {get_total_energy(board)}")
    for row in range(-1, 6):
        for col in range(-1, 12):
            try:
                spot = board[row, col]
            except KeyError:
                print("#", end="")
            else:
                if spot is None:
                    print(".", end="")
                else:
                    print(spot, end="")
        print("")
    print()


def get_next_steps(board: Board) -> List[Board]:
    # Here, we look for any opportunities to move a hallway pod to its target column
    clear_hallway = True
    while clear_hallway:
        clear_hallway = False  # Don't repeat unless we were successful in moving a pod

        for (row, col), pod in board.items():
            if pod is None or row > 0:
                continue

            target_col = SLOT_MAP[pod.char]
            target_row = None
            for target_row in range(4, 0, -1):
                try:
                    room_pod = board[target_row, target_col]
                except KeyError:
                    continue

                if room_pod is None:
                    break  # target_row is correct
                if room_pod.char == pod.char:
                    continue  # to next highest spot
                else:
                    target_row = None
                    break

            if target_row is None:
                continue

            if (
                energy := get_energy_to_move(
                    board, (row, col), (target_row, target_col)
                )
            ) is not None:
                new_pod = Pod(char=pod.char, energy=pod.energy + energy)
                board[target_row, target_col] = new_pod
                board[row, col] = None
                clear_hallway = True
                break

    if is_winning(board):
        return [board]

    movable_room_pawns = []
    for target, col in SLOT_MAP.items():
        # Find the highest open slot, ensuring all below have correct char
        col_pods = []
        for row in range(4, 0, -1):
            try:
                room_pod = board[row, col]
            except KeyError:
                continue
            else:
                if room_pod is not None:
                    col_pods.append((row, col, room_pod))

        if any(p.char != target for _, _, p in col_pods):
            r, c, p = col_pods[-1]
            movable_room_pawns.append((r, c))

    open_hallway_targets = [
        (row, col)
        for (row, col), char in board.items()
        if row == 0 and char is None and col not in {2, 4, 6, 8}
    ]

    boards = []
    for source_coords, target_coords in itertools.product(
        movable_room_pawns, open_hallway_targets
    ):
        if (
            energy := get_energy_to_move(board, source_coords, target_coords)
        ) is not None:
            new_board = dict(board)
            source_pod = board[source_coords]
            assert source_pod is not None
            new_board[target_coords] = Pod(source_pod.char, source_pod.energy + energy)
            new_board[source_coords] = None
            boards.append(new_board)

    return boards


def get_energy_to_move(board: Board, source: Coords, target: Coords) -> Optional[int]:
    """Returns the energy cost to move from source to target, or None of move is not allowed."""
    source_row, source_col = source
    target_row, target_col = target

    # Check that every hallway space between the source and target are empty
    sgn = (target_col - source_col) // abs(target_col - source_col)
    for col in range(source_col + sgn, target_col + sgn, sgn):
        if board[0, col] is not None:
            return None
    num_steps = abs(target_col - source_col) + abs(target_row - source_row)
    source_pod = board[source]
    assert source_pod is not None
    return num_steps * COST_MAP[source_pod.char]


def is_winning(board: Board) -> bool:
    for target, col in SLOT_MAP.items():
        for row in range(1, 5):
            try:
                pod = board[row, col]
            except KeyError:
                continue

            if pod is None or pod.char != target:
                return False
    return True


def get_total_energy(board: Board) -> int:
    return sum(pod.energy for pod in board.values() if pod is not None)


def find_min_energy(input_board: Board) -> int:
    min_energy = float(100_000)

    def _find_min_energy(board: Board, total_energy: int = 0) -> None:
        nonlocal min_energy
        # print_board(board)
        if is_winning(board):
            # total_energy = get_total_energy(board)
            min_energy = min(min_energy, total_energy)
            # print(f"Found a winning board with {total_energy} energy!")
            return

        if total_energy > min_energy:
            # print("Board exceeds current minimum!")
            return

        alternatives = get_next_steps(board)
        if not alternatives:
            return

        for i, alt in enumerate(alternatives):
            _find_min_energy(alt, get_total_energy(alt))

    _find_min_energy(input_board)
    return int(min_energy)


def calculate_part1(input_str: str) -> int:
    board = parse(input_str)  # noqa: F841
    return find_min_energy(board)


def calculate_part2(input_str: str) -> int:
    board = parse(input_str)  # noqa: F841
    for col, chars in zip([2, 4, 6, 8], ["DD", "CB", "BA", "AC"]):
        board[4, col] = board[2, col]
        board[2, col] = Pod(char=chars[0])
        board[3, col] = Pod(char=chars[1])
    return find_min_energy(board)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
