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
    path = [start]
    while (joint := joints[row + dx, col + dy]) != "S":
        if (dx, dy) not in TOPO_MAP[joint]:
            raise ValueError("Dead End")

        (row, col) = (row + dx, col + dy)
        (dx, dy) = TOPO_MAP[joint][dx, dy]
        path.append((row, col))

    return path


def find_path(joints, start):
    # Loop through the four adjacent neighbors to see if there is a joint
    for step in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        try:
            path = trace_path(joints, start, step)
        except (KeyError, ValueError):
            # Either we started where there was no joint, or we hit a dead end
            continue
        else:
            return path


def calculate_part1(input_str: str) -> int:
    start, joints = parse(input_str)  # noqa: F841

    path = find_path(joints, start)
    path_length = len(path)
    return path_length // 2 + path_length % 2


def count_interior_tiles(joints, path):
    loop = set(path)  # Used to more efficiently check membership
    enclosed = set()

    for curr, next in zip(path, path[1:]):
        (dx, dy) = (next[0] - curr[0], next[1] - curr[1])

        # 90 deg, counter-clockwise
        search_dir = dy, -dx

        # Search in that direction until we hit a part of the loop
        # We need to search from both the current and next location
        # This covers corners, where the direction will change and
        # next -> curr.
        for xy in [curr, next]:
            while (xy := (xy[0] + search_dir[0], xy[1] + search_dir[1])) not in loop:
                enclosed.add(xy)
                if max(max(xy), abs(min(xy))) > 1000:
                    # If we go off the board, we need to go the other way through the loop
                    return count_interior_tiles(joints, path[::-1])

    return len(enclosed)


def calculate_part2(input_str: str) -> int:
    start, joints = parse(input_str)  # noqa: F841
    path = find_path(joints, start)
    return count_interior_tiles(joints, path)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
