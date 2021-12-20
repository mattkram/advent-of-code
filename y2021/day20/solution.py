from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"

Algorithm = List[bool]
Image = Dict[Tuple[int, int], bool]


def parse(input_str: str) -> Tuple[Algorithm, Image]:
    # print()
    algorithm, _, image = input_str.strip().partition("\n\n")
    algorithm = "".join(line.strip() for line in algorithm.splitlines())
    algorithm_list = [c == "#" for c in algorithm]
    # print(algorithm)
    image_dict = {}
    row = 0
    for line in image.splitlines():
        if not line.strip():
            continue
        for col, char in enumerate(line.strip()):
            image_dict[row, col] = char == "#"
        row += 1
    return algorithm_list, image_dict


def print_image(image: Image) -> None:
    min_row, min_col = min(image.keys())
    max_row, max_col = max(image.keys())
    for row in range(min_row - 5, max_row + 6):
        for col in range(min_col - 5, max_col + 6):
            pixel = "🟡" if image.get((row, col), False) else "⚫"
            print(pixel, end="")
        print()
    print()


def apply_algorithm(algorithm: Algorithm, image: Image, default: bool = False) -> Image:
    min_row, min_col = min(image.keys())
    max_row, max_col = max(image.keys())
    new_image = {}
    for row in range(min_row - 1, max_row + 2):
        for col in range(min_col - 1, max_col + 2):
            pixels = []
            for d_row in [-1, 0, 1]:
                for d_col in [-1, 0, 1]:
                    pixel = image.get((row + d_row, col + d_col), default)
                    pixels.append(int(pixel))
            index = int("".join(str(p) for p in pixels), 2)
            new_image[row, col] = algorithm[index]
    return new_image


def calculate(input_str: str, num_it: int) -> int:
    algorithm, image = parse(input_str)  # noqa: F841
    default = False
    for _ in range(num_it):
        image = apply_algorithm(algorithm, image, default)
        if algorithm[0]:
            # Need to change the default if the 0 bit pattern (in infinity)
            # will flip all the infinite bits to lit
            default = not default
    print()
    print_image(image)

    return sum(image.values())


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str, num_it=2)}")
        print(f"The answer to part 2 is {calculate(input_str, num_it=50)}")


if __name__ == "__main__":
    main()
