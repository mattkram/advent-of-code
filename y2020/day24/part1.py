from collections import defaultdict
from collections import deque
from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple

import pytest


ParsedInput = List[List[str]]
Coords = Tuple[int, int]

INPUTS_FILE = Path(__file__).parent / "input.txt"
STEP_MAP = {
    "e": (2, 0),
    "w": (-2, 0),
    "ne": (1, 1),
    "nw": (-1, 1),
    "se": (1, -1),
    "sw": (-1, -1),
}


def parse(input_str: str) -> ParsedInput:
    data: List[List[str]] = []
    for line in input_str.strip().splitlines():
        chars = deque(line.strip())
        instruction: List[str] = []
        while chars:
            token = chars.popleft()
            if token in "ns":
                token += chars.popleft()
            instruction.append(token)
        data.append(instruction)
    return data


def get_coordinates(instructions: List[str]) -> Tuple[int, int]:
    row, col = 0, 0
    for instruction in instructions:
        dx, dy = STEP_MAP[instruction]
        row += dx
        col += dy
    return row, col


def calculate(data: ParsedInput) -> int:
    is_black: Dict[Coords, bool] = defaultdict(lambda: False)
    for instructions in data:
        coordinates = get_coordinates(instructions)
        is_black[coordinates] ^= True
    return sum(is_black.values())


TEST_INPUTS = [
    (
        """
        sesenwnenenewseeswwswswwnenewsewsw
        neeenesenwnwwswnenewnwwsewnenwseswesw
        seswneswswsenwwnwse
        nwnwneseeswswnenewneswwnewseswneseene
        swweswneswnenwsewnwneneseenw
        eesenwseswswnenwswnwnwsewwnwsene
        sewnenenenesenwsewnenwwwse
        wenwwweseeeweswwwnwwe
        wsweesenenewnwwnwsenewsenwwsesesenwne
        neeswseenwwswnwswswnw
        nenwswwsewswnenenewsenwsenwnesesenew
        enewnwewneswsewnwswenweswnenwsenwsw
        sweneswneswneneenwnewenewwneswswnese
        swwesenesewenwneswnwwneseswwne
        enesenwswwswneneswsenwnewswseenwsese
        wnwnesenesenenwwnenwsewesewsesesew
        nenewswnwewswnenesenwnesewesw
        eneswnwswnwsenenwnwnwwseeswneewsenese
        neswnwewnwnwseenwseesewsenwsweewe
        wseweeenwnesenwwwswnew
        """,
        10,
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> int:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
