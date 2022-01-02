from pathlib import Path
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

INPUTS_FILE = Path(__file__).parent / "input.txt"


# Extracted from input
CONSTANTS = [
    (1, 14, 12),
    (1, 15, 7),
    (1, 12, 1),
    (1, 11, 2),
    (26, -5, 4),
    (1, 14, 15),
    (1, 15, 11),
    (26, -13, 5),
    (26, -16, 3),
    (26, -8, 9),
    (1, 15, 2),
    (26, -8, 3),
    (26, 0, 3),
    (26, -4, 11),
]

Instruction = Tuple[str, str, Optional[Union[int, str]]]


def parse(input_str: str) -> List[Instruction]:
    instructions = []
    for line in input_str.strip().splitlines():
        if not line.strip():
            continue
        instruction, *args = line.strip().split()
        target = str(args[0])
        value: Optional[Union[int, str]]
        if instruction == "inp":
            value = None
        else:
            try:
                value = int(args[1])
            except ValueError:
                value = args[1]
        instructions.append((instruction, target, value))
    return instructions


def compute(instructions: List[Instruction], model_number: str) -> int:
    digits = [int(i) for i in str(model_number)]

    state = {"w": 0, "x": 0, "y": 0, "z": 0}

    for instruction, var_name, value in instructions:
        if instruction == "inp":
            state[var_name] = digits.pop(0)
            continue

        assert value is not None
        if isinstance(value, str):
            value = state[value]

        if instruction == "add":
            state[var_name] += value
        elif instruction == "mul":
            state[var_name] *= value
        elif instruction == "div":
            state[var_name] //= value
        elif instruction == "mod":
            state[var_name] %= value
        elif instruction == "eql":
            state[var_name] = int(state[var_name] == value)
        else:
            raise ValueError("Unreachable")
    return state["z"]


def compute_manual(model_number: str) -> int:
    digits = [int(i) for i in str(model_number)]

    z = 0
    for w, (c_1, c_2, c_3) in zip(digits, CONSTANTS):
        if z % 26 + c_2 == w:
            z //= c_1
        else:
            z = (z // c_1) * 26 + w + c_3

    return z


def solve_inverse_problem() -> List[Set[int]]:
    allowable_z = [{0}]
    for c_1, c_2, c_3 in CONSTANTS[:0:-1]:
        options = set()
        for z in allowable_z[0]:
            for i in range(c_1):
                z_prev = z * c_1 + i
                w = z_prev % 26 + c_2
                if 1 <= w <= 9:
                    options.add(z_prev)

            # Min occurs when w == 9
            z_min = c_1 * (z - 9 - c_3 + 25) // 26

            # Max occurs when w == 1
            z_max = c_1 * (z - 1 - c_3 + 26) // 26
            options.update(range(z_min, z_max))

        allowable_z.insert(0, options)

    return allowable_z


def calculate(find_max: bool = True) -> int:
    options = solve_inverse_problem()

    def _find_next_digit(digits: Optional[List[int]] = None) -> List[int]:
        digits = digits or []
        idx = len(digits)

        if idx == len(options):
            return digits

        digit_search = range(9, 0, -1) if find_max else range(1, 10)
        for digit in digit_search:
            new_digits = digits + [digit]
            z_new = compute_manual("".join(map(str, new_digits)))
            if z_new in options[idx]:
                return _find_next_digit(digits=new_digits)

        raise ValueError("Unreachable")

    result_digits = _find_next_digit()
    return int("".join(map(str, result_digits)))


def main() -> None:
    print(f"The answer to part 1 is {calculate(find_max=True)}")
    print(f"The answer to part 2 is {calculate(find_max=False)}")


if __name__ == "__main__":
    main()
