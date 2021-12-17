from pathlib import Path
from typing import Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    x_str, _, y_str = input_str.strip().replace("target area: ", "").partition(", ")
    x_min_str, _, x_max_str = x_str[2:].partition("..")
    y_min_str, _, y_max_str = y_str[2:].partition("..")
    return (int(x_min_str), int(x_max_str)), (int(y_min_str), int(y_max_str))


def calculate_part1(input_str: str) -> int:
    (x_min, x_max), (y_min, y_max) = parse(input_str)  # noqa: F841

    overall_max_y = 0
    for v_xo in range(101):
        for v_yo in range(-11, 1001):
            v_x, v_y = v_xo, v_yo
            max_y = 0
            x, y = 0, 0
            hit_target = False
            while y > y_min and x <= x_max:
                x += v_x
                y += v_y
                max_y = max(y, max_y)

                if x_min <= x <= x_max and y_min <= y <= y_max:
                    hit_target = True
                    break

                v_x -= v_x // abs(v_x) if v_x != 0 else 0
                v_y -= 1

            if hit_target:
                overall_max_y = max(overall_max_y, max_y)

    return overall_max_y


def calculate_part2(input_str: str) -> int:
    (x_min, x_max), (y_min, y_max) = parse(input_str)  # noqa: F841

    num_hits = 0
    for v_xo in range(1001):
        for v_yo in range(-501, 1501):
            v_x, v_y = v_xo, v_yo
            max_y = 0
            x, y = 0, 0
            hit_target = False
            while y > y_min and x <= x_max:
                x += v_x
                y += v_y
                max_y = max(y, max_y)

                if x_min <= x <= x_max and y_min <= y <= y_max:
                    hit_target = True
                    break

                v_x -= v_x // abs(v_x) if v_x != 0 else 0
                v_y -= 1

            if hit_target:
                num_hits += 1

    return num_hits


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
