from pathlib import Path
from typing import NamedTuple

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> list[int]:
    obstructions = {}
    lines = [s.strip() for s in input_str.splitlines() if s.strip()]
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c != ".":
                obstructions[j, i] = c

    max_row = len(lines)
    max_col = len(lines[0])
    return obstructions, Coord(max_col, max_row)


class Coord(NamedTuple):
    x: int
    y: int


class Beam:
    def __init__(self, position, velocity):
        self.position = Coord(*position)
        self.velocity = Coord(*velocity)

    def move(self):
        self.position = Coord(
            x=self.position.x + self.velocity.x,
            y=self.position.y + self.velocity.y,
        )


def calculate_part1(input_str: str) -> int:
    obstructions, dims = parse(input_str)
    beams = {Beam(position=(-1, 0), velocity=(1, 0))}
    history = set()
    while beams:
        for beam in set(beams):
            # Move the beam forward
            beam.move()

            # If we've exceeded the bounds of the mirror, we can remove the beam.
            if not (0 <= beam.position.x < dims.x and 0 <= beam.position.y < dims.y):
                beams.remove(beam)
                continue

            # If we've been here before, with same velocity, we've already solved it so
            # we can remove the beam.
            bh = (beam.position, beam.velocity)
            if bh in history:
                beams.remove(beam)
                continue
            history.add(bh)

            # Now we decide what to do based on hitting an obstruction.
            o = obstructions.get(beam.position)
            if o == "|":
                if beam.velocity.x != 0:
                    beams.update(
                        {
                            Beam(position=beam.position, velocity=(0, 1)),
                            Beam(position=beam.position, velocity=(0, -1)),
                        }
                    )
                    beams.remove(beam)
            elif o == "-":
                if beam.velocity.y != 0:
                    beams.update(
                        {
                            Beam(position=beam.position, velocity=(1, 0)),
                            Beam(position=beam.position, velocity=(-1, 0)),
                        }
                    )
                    beams.remove(beam)
            elif o == "/":
                if beam.velocity.x == 1:
                    beam.velocity = Coord(x=0, y=-1)
                elif beam.velocity.x == -1:
                    beam.velocity = Coord(x=0, y=1)
                elif beam.velocity.y == -1:
                    beam.velocity = Coord(x=1, y=0)
                else:
                    beam.velocity = Coord(x=-1, y=0)
            elif o == "\\":
                if beam.velocity.x == 1:
                    beam.velocity = Coord(x=0, y=1)
                elif beam.velocity.x == -1:
                    beam.velocity = Coord(x=0, y=-1)
                elif beam.velocity.y == -1:
                    beam.velocity = Coord(x=-1, y=0)
                else:
                    beam.velocity = Coord(x=1, y=0)
            else:
                # The space is empty
                continue

    return len(set(pos for (pos, _) in history))


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    raise ValueError("Cannot find an answer")


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
