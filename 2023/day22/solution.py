from pathlib import Path
from typing import List


INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[int]:
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    bricks = []
    for line in lines:
        left, right = line.split("~")
        left = tuple(int(c) for c in left.split(","))
        right = tuple(int(c) for c in right.split(","))

        cubes = []
        x_min, x_max = min(left[0], right[0]), max(left[0], right[0])
        y_min, y_max = min(left[1], right[1]), max(left[1], right[1])
        z_min, z_max = min(left[2], right[2]), max(left[2], right[2])
        dims = (x_max + 1 - x_min, y_max + 1 - y_min, z_max + 1 - z_min)
        if 1 not in dims:
            raise ValueError(f"Brick is not one-dimensional: {dims}")
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    cubes.append((x, y, z))
        bricks.append(cubes)

    return bricks


def move_down(bricks, exit_early=False):
    """Continuously move bricks downward one step at a time until they settle."""
    did_move = False
    while True:
        has_moved = False
        for i, brick in enumerate(bricks):
            if any(z == 1 for _, _, z in brick):
                # On the ground
                continue

            other_cubes = set()
            for j, b in enumerate(bricks):
                if i == j:
                    continue
                other_cubes.update(set(b))

            one_below = {(x, y, z - 1) for x, y, z in brick}
            intersection = one_below & other_cubes
            if not intersection:
                # Move the brick down
                has_moved = True
                did_move = True
                if exit_early:
                    return True
                bricks[i] = list(one_below)

        if not has_moved:
            break
    return did_move


def calculate_part1(input_str: str) -> int:
    bricks = parse(input_str)
    # move_down(bricks)

    result = 0
    for i in range(len(bricks)):
        # First make a copy but ignore one of the bricks
        bricks_copy = [list(brick) for j, brick in enumerate(bricks) if i != j]

        did_move = move_down(bricks_copy, exit_early=True)
        if not did_move:
            result += 1
    return result


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
