from itertools import combinations
from itertools import product
from pathlib import Path
from typing import Any
from typing import List
from typing import Set

import pytest


INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List["Tile"]


class Tile:
    def __init__(self, id_num: int, pixels: List[List[str]]):
        self.id = id_num
        self.pixels = pixels
        self.neighbors: Set[Tile] = set()

    def flip_lr(self) -> None:
        self.pixels = [row[::-1] for row in self.pixels]

    def flip_ud(self) -> None:
        self.pixels = self.pixels[::-1]

    def rotate(self) -> None:
        new_pixels = []
        for col in range(len(self.pixels[0])):
            row_pixels = []
            for row in range(len(self.pixels)):
                row_pixels.append(self.pixels[row][col])
            new_pixels.append(row_pixels)
        self.pixels = new_pixels
        self.flip_ud()

    @property
    def left(self) -> List[str]:
        return [row[0] for row in self.pixels]

    @property
    def right(self) -> List[str]:
        return [row[-1] for row in self.pixels]

    @property
    def top(self) -> List[str]:
        return list(self.pixels[0])

    @property
    def bottom(self) -> List[str]:
        return list(self.pixels[-1])

    @property
    def edges(self) -> List[List[str]]:
        return [self.left, self.right, self.top, self.bottom]

    @property
    def num_neighbors(self) -> int:
        return len(self.neighbors)

    def is_neighbor(self, other: "Tile") -> bool:
        if self is other:
            return False

        for this_edge, other_edge in product(self.edges, other.edges):
            if this_edge == other_edge or this_edge == other_edge[::-1]:
                print(f"{other.id} is a neighbor of {self.id}")
                self.neighbors.add(other)
                other.neighbors.add(self)
                return True
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Tile) and self.id == other.id


def parse(input_str: str) -> ParsedInput:
    tiles = []
    for tile_str in input_str.strip().split("\n\n"):
        tile_num_str, *pixel_str = tile_str.strip().splitlines()
        tile_num = int(tile_num_str[5:-1])
        pixels = [list(p.strip()) for p in pixel_str]
        tiles.append(Tile(tile_num, pixels))
    return tiles


def calculate(tiles: ParsedInput) -> int:
    for tile, other_tile in combinations(tiles, 2):
        tile.is_neighbor(other_tile)

    result = 1
    for tile in tiles:
        if tile.num_neighbors == 2:
            result *= tile.id

    return result


TEST_INPUTS = [
    (
        """
        Tile 2311:
        ..##.#..#.
        ##..#.....
        #...##..#.
        ####.#...#
        ##.##.###.
        ##...#.###
        .#.#.#..##
        ..#....#..
        ###...#.#.
        ..###..###

        Tile 1951:
        #.##...##.
        #.####...#
        .....#..##
        #...######
        .##.#....#
        .###.#####
        ###.##.##.
        .###....#.
        ..#.#..#.#
        #...##.#..

        Tile 1171:
        ####...##.
        #..##.#..#
        ##.#..#.#.
        .###.####.
        ..###.####
        .##....##.
        .#...####.
        #.##.####.
        ####..#...
        .....##...

        Tile 1427:
        ###.##.#..
        .#..#.##..
        .#.##.#..#
        #.#.#.##.#
        ....#...##
        ...##..##.
        ...#.#####
        .#.####.#.
        ..#..###.#
        ..##.#..#.

        Tile 1489:
        ##.#.#....
        ..##...#..
        .##..##...
        ..#...#...
        #####...#.
        #..#.#.#.#
        ...#.#.#..
        ##.#...##.
        ..##.##.##
        ###.##.#..

        Tile 2473:
        #....####.
        #..#.##...
        #.##..#...
        ######.#.#
        .#...#.#.#
        .#########
        .###.#..#.
        ########.#
        ##...##.#.
        ..###.#.#.

        Tile 2971:
        ..#.#....#
        #...###...
        #.#.###...
        ##.##..#..
        .#####..##
        .#..####.#
        #..#.#..#.
        ..####.###
        ..#.#.###.
        ...#.#.#.#

        Tile 2729:
        ...#.#.#.#
        ####.#....
        ..#.#.....
        ....#..#.#
        .##..##.#.
        .#.####...
        ####.#.#..
        ##.####...
        ##..#.##..
        #.##...##.

        Tile 3079:
        #.#.#####.
        .#..######
        ..#.......
        ######....
        ####.#..#.
        .#...#.##.
        #.#####.##
        ..#.###...
        ..#.......
        ..#.###...
        """,
        20899048083289,
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
