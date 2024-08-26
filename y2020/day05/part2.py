from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


def get_val(string: str, keys: str) -> int:
    return sum(keys.index(v) * 2**n for n, v in enumerate(reversed(string)))


def calculate(input_str: str) -> int:
    seats = [line.strip() for line in input_str.split()]
    seats_assigned = []
    for seat in seats:
        row = get_val(seat[:7], "FB")
        col = get_val(seat[7:], "LR")
        seat_num = 8 * row + col
        seats_assigned.append(seat_num)

    seats_assigned.sort()
    seat_range = set(range(min(seats_assigned), max(seats_assigned)))
    diff = seat_range.difference(set(seats_assigned))
    my_seat = list(diff)[0]
    return my_seat


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(fp.read())


if __name__ == "__main__":
    print(f"The answer is {main()}")
