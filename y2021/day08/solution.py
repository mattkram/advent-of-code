import itertools
from pathlib import Path
from typing import List
from typing import Tuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> List[Tuple[List[str], List[str]]]:
    data = []
    for line in input_str.splitlines():
        if not line.strip():
            continue
        first, second = line.split("|")
        data.append((first.split(), second.split()))
    return data


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    result = 0
    for first, second in data:
        for item in second:
            if len(item) in {2, 3, 4, 7}:
                result += 1
    return result


def extract_with_length(inputs: List[str], n: int) -> List[str]:
    return [i for i in inputs if len(i) == n]


digits = {
    0: [0, 1, 2, 4, 5, 6],
    1: [2, 5],
    2: [0, 2, 3, 4, 6],
    3: [0, 2, 3, 5, 6],
    4: [1, 2, 3, 5],
    5: [0, 1, 3, 5, 6],
    6: [0, 1, 3, 4, 5, 6],
    7: [0, 2, 5],
    8: [0, 1, 2, 3, 4, 5, 6],
    9: [0, 1, 2, 3, 5, 6],
}


def decode(inputs: List[str], outputs: List[str]) -> int:
    options = [set("abcdefg") for _ in range(7)]

    val = extract_with_length(inputs, 2)[0]
    options[2] &= set(val)
    options[5] &= set(val)
    for i in {0, 1, 3, 4, 6}:
        options[i] -= set(val)

    val = extract_with_length(inputs, 3)[0]
    options[0] &= set(val) - options[2]
    for i in {1, 2, 3, 4, 5, 6}:
        options[i] -= options[0]

    val = extract_with_length(inputs, 4)[0]
    options[1] &= set(val) - options[2]
    options[3] &= set(val) - options[2]

    options[4] -= options[1]
    options[6] -= options[1]

    options_list = [list(i) for i in options]
    for a, b, c in itertools.product(options_list[1], options_list[2], options_list[4]):
        ii = [v for v in options_list[1] if v != a][0]
        jj = [v for v in options_list[2] if v != b][0]
        kk = [v for v in options_list[4] if v != c][0]
        mapping = [options_list[0][0], a, b, ii, c, jj, kk]

        found_match = True
        for digit, lines in digits.items():
            chars = set(mapping[n] for n in lines)
            if not any(chars == set(input_) for input_ in inputs):
                found_match = False

        if found_match:
            result = 0
            for output in outputs:
                for digit, lines in digits.items():
                    chars = set(mapping[n] for n in lines)
                    if chars == set(output):
                        result *= 10
                        result += digit
            return result
    return -1


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    result = 0
    for inputs, output in data:
        result += decode(inputs, output)
    return result


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
