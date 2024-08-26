from pathlib import Path
from typing import Dict

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"
EXPECTED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
EXPECTED_FIELDS.remove("cid")
EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


class ValidationError(Exception):
    pass


def validate(passport: Dict[str, str]) -> None:
    fields = set(passport.keys())

    def error(field: str) -> None:
        raise ValidationError(f"{field} invalid: {passport[field]}")

    if not fields.issuperset(EXPECTED_FIELDS):
        raise ValidationError("Missing expected field(s)")

    if not 1920 <= int(passport["byr"]) <= 2002:
        error("byr")

    if not 2010 <= int(passport["iyr"]) <= 2020:
        error("iyr")

    if not 2020 <= int(passport["eyr"]) <= 2030:
        error("eyr")

    if (hgt_str := passport["hgt"]).endswith("cm"):
        if not 150 <= int(hgt_str[:-2]) <= 193:
            error("hgt")
    elif (hgt_str := passport["hgt"]).endswith("in"):
        if not 59 <= int(hgt_str[:-2]) <= 76:
            error("hgt")
    else:
        error("hgt")

    hash_, hcl = passport["hcl"][0], passport["hcl"][1:]
    if hash_ != "#" or len(hcl) != 6 or not set(hcl).issubset(set("0123456789abcdef")):
        error("hcl")

    if passport["ecl"] not in EYE_COLORS:
        error("ecl")

    pid = passport["pid"]
    if len(pid) != 9 or any(not s.isdigit() for s in pid):
        error("pid")


def calculate(input_str: str) -> int:
    # Split into chunks based on a blank line
    lines = [s.strip() for s in input_str.split("\n")]
    lines = "\n".join(lines).split("\n\n")
    num_valid = 0
    for line in lines:
        kv_str = [s.strip().partition(":") for s in line.split()]
        passport = {key: value for key, _, value in kv_str}
        try:
            validate(passport)
        except ValidationError:
            continue
        num_valid += 1
    return num_valid


TEST_INPUTS = [
    (
        """
        eyr:1972 cid:100
        hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

        iyr:2019
        hcl:#602927 eyr:1967 hgt:170cm
        ecl:grn pid:012533040 byr:1946

        hcl:dab227 iyr:2012
        ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

        hgt:59cm ecl:zzz
        eyr:2038 hcl:74454a iyr:2023
        pid:3556412378 byr:2007
        """,
        0,
    ),
    (
        """
        pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
        hcl:#623a2f

        eyr:2029 ecl:blu cid:129 byr:1989
        iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

        hcl:#888785
        hgt:164cm byr:2001 iyr:2015 cid:88
        pid:545766238 ecl:hzl
        eyr:2022

        iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
        """,
        4,
    ),
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(fp.read())


if __name__ == "__main__":
    print(f"The answer is {main()}")
