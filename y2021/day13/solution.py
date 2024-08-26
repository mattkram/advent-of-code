from pathlib import Path
from typing import List, Set, Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:
    cells_str, folds_str = input_str.strip().split("\n\n")

    cells = set()
    for line in cells_str.splitlines():
        x, y = (int(s) for s in line.strip().split(","))
        cells.add((x, y))

    folds = []
    for line in folds_str.splitlines():
        direction, value = line.replace("fold along ", "").split("=")
        folds.append((direction, int(value)))

    return cells, folds


def calculate_part1(input_str: str) -> int:
    cells, folds = parse(input_str)  # noqa: F841

    dim, value = folds[0]
    new_cells = set()
    for x, y in cells:
        if dim == "y":
            y = value - abs(y - value)
        elif dim == "x":
            x = value - abs(x - value)

        new_cells.add((x, y))

    return len(new_cells)


def calculate_part2(input_str: str) -> str:
    data = parse(input_str)  # noqa: F841
    cells, folds = parse(input_str)  # noqa: F841

    for fold in folds:
        dim, value = fold
        new_cells = set()
        for x, y in cells:
            if dim == "y":
                y = value - abs(y - value)
            elif dim == "x":
                x = value - abs(x - value)

            new_cells.add((x, y))
        cells = new_cells

    max_x = max(cell[0] for cell in cells)
    max_y = max(cell[1] for cell in cells)
    lines = []
    for row in range(max_y + 1):
        line = []
        for col in range(max_x + 1):
            if (col, row) in cells:
                line.append("🟡")
            else:
                line.append("⚫")
        lines.append("".join(line))
    return "\n".join(lines)


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is: {calculate_part1(input_str)}")
        print(f"The answer to part 2 is:\n{calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
