from pathlib import Path


INPUTS_FILE = Path(__file__).parent / "input.txt"

# A mapping of the allowable (dx, dy) to enter a type of joint from either end
# The value is the (dx, dy) that exits the pipe.
TOPO_MAP = {
    "|": {
        (0, 1): (0, 1),
        (0, -1): (0, -1),
    },
    "-": {
        (1, 0): (1, 0),
        (-1, 0): (-1, 0),
    },
    "F": {
        (0, -1): (1, 0),
        (-1, 0): (0, 1),
    },
    "J": {
        (0, +1): (-1, 0),
        (+1, 0): (0, -1),
    },
    "L": {
        (0, +1): (1, 0),
        (-1, 0): (0, -1),
    },
    "7": {
        (0, -1): (-1, 0),
        (+1, 0): (0, 1),
    },
}


def parse(input_str: str) -> tuple[tuple[int, int], dict[tuple[int, int], str]]:
    joints = {}
    start = None

    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    for j, line in enumerate(lines):
        for i, s in enumerate(line):
            if s == "S":
                start = (i, j)
            if s == ".":
                continue
            joints[(i, j)] = s
    return start, joints


def trace_path(joints, start, first_step):
    row, col = start
    dx, dy = first_step
    num_steps = 0
    while (joint := joints[row + dx, col + dy]) != "S":
        if (dx, dy) not in TOPO_MAP[joint]:
            raise ValueError("Dead End")

        (row, col) = (row + dx, col + dy)
        (dx, dy) = TOPO_MAP[joint][dx, dy]
        num_steps += 1
    return num_steps


def calculate_part1(input_str: str) -> int:
    start, joints = parse(input_str)  # noqa: F841

    # Loop through the four adjacent neighbors to see if there is a joint
    path_lengths = []
    for step in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        try:
            path_length = trace_path(joints, start, step)
        except (KeyError, ValueError):
            # Either we started where there was no joint, or we hit a dead end
            continue
        else:
            path_lengths.append(path_length)

    max_length = max(path_lengths)
    return max_length // 2 + max_length % 2


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
