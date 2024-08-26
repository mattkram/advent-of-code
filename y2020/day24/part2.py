from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Tuple

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
    # True means tile is black
    tile_map: Dict[Coords, bool] = defaultdict(lambda: False)
    for instructions in data:
        coordinates = get_coordinates(instructions)
        tile_map[coordinates] ^= True

    for day in range(100):
        tiles_to_flip = set()

        # Visit all black cells first, since defaultdict will ensure
        # neighbors are marked as white as visited if not in map
        for (row, col), is_black in list(tile_map.items()):
            if not is_black:
                continue
            num_black_neighbors = sum(
                tile_map[row + dx, col + dy] for dx, dy in STEP_MAP.values()
            )
            if num_black_neighbors not in {1, 2}:
                tiles_to_flip.add((row, col))

        # Now visit all the white tiles, since the black ones will have been padded
        for (row, col), is_black in list(tile_map.items()):
            if is_black:
                continue
            num_black_neighbors = sum(
                tile_map[row + dx, col + dy] for dx, dy in STEP_MAP.values()
            )
            if num_black_neighbors == 2:
                tiles_to_flip.add((row, col))

        for coords in tiles_to_flip:
            tile_map[coords] ^= True

    return sum(tile_map.values())


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
        2208,
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
