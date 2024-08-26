from pathlib import Path

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"
EXPECTED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
EXPECTED_FIELDS.remove("cid")


def calculate(input_str: str) -> int:
    # Split into chunks based on a blank line
    lines = [s.strip() for s in input_str.split("\n\n")]

    num_valid = 0
    for line in lines:
        kv_str = [s.strip().partition(":") for s in line.split()]
        passport = {key: value for key, _, value in kv_str}
        fields = set(passport.keys())
        is_valid = fields.issuperset(EXPECTED_FIELDS)
        num_valid += int(is_valid)
    return num_valid


TEST_INPUTS = [
    (
        """\
        ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        byr:1937 iyr:2017 cid:147 hgt:183cm

        iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
        hcl:#cfa07d byr:1929

        hcl:#ae17e1 iyr:2013
        eyr:2024
        ecl:brn pid:760753108 byr:1931
        hgt:179cm

        hcl:#cfa07d eyr:2025 pid:166559648
        iyr:2011 ecl:brn hgt:59in
        """,
        2,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(fp.read())


if __name__ == "__main__":
    print(f"The answer is {main()}")
