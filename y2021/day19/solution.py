import itertools
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Generator, List, NamedTuple, Optional

INPUTS_FILE = Path(__file__).parent / "input.txt"

NUM = r"-?\d+"


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: Any) -> "Coordinate":
        if not isinstance(other, Coordinate):
            raise TypeError
        return Coordinate(other.x + self.x, other.y + self.y, other.z + self.z)

    def __sub__(self, other: Any) -> "Coordinate":
        if not isinstance(other, Coordinate):
            raise TypeError
        return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Coordinate):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z


class ScannerReport:
    def __init__(self) -> None:
        self.scanner_number = -1
        self.orientation = 0
        self.readings: List[Coordinate] = []
        self.position: Optional[Coordinate] = None  # Relative to scanner 0

    def __repr__(self) -> str:
        return (
            f"ScannerReport(scanner_number={self.scanner_number}, "
            f"position={self.position}, "
            f"orientation={self.orientation})"
        )

    def add_reading(self, coords: Coordinate) -> None:
        self.readings.append(coords)

    def rotations(self) -> Generator["ScannerReport", None, None]:
        # I believe we would end up

        for i, (x_mult, y_mult, z_mult, indices) in enumerate(
            itertools.product(
                [-1, 1], [-1, 1], [-1, 1], itertools.permutations([0, 1, 2])
            )
        ):
            # print(y_mult, z_mult, indices)
            scanner_report = ScannerReport()
            scanner_report.scanner_number = self.scanner_number
            scanner_report.orientation = i

            for coords in self.readings:
                new_coords = Coordinate(
                    x_mult * coords[indices[0]],
                    y_mult * coords[indices[1]],
                    z_mult * coords[indices[2]],
                )
                scanner_report.add_reading(new_coords)

            yield scanner_report

    def _rotations(self) -> Generator["ScannerReport", None, None]:
        # I believe we would end up
        prelims = [
            dict(z_rot=0),
            dict(z_rot=90),
            dict(z_rot=180),
            dict(z_rot=270),
            dict(y_rot=90),
            dict(y_rot=270),
        ]
        for i, (prelim, x_rot) in enumerate(
            itertools.product(prelims, [0, 90, 180, 270])
        ):
            # print(y_mult, z_mult, indices)
            scanner_report = ScannerReport()
            scanner_report.scanner_number = self.scanner_number
            scanner_report.orientation = i

            for coords in self.readings:
                new_coords = rotate(coords, x_rot=x_rot, **prelim)
                scanner_report.add_reading(new_coords)

            yield scanner_report


def rotate(
    coords: Coordinate, x_rot: float = 0, y_rot: float = 0, z_rot: float = 0
) -> Coordinate:
    # Rotate around z
    # Rotate around y
    # Rotate around x
    x_rot *= math.pi / 180
    y_rot *= math.pi / 180
    z_rot *= math.pi / 180

    coords = Coordinate(
        x=int(coords.x * math.cos(z_rot) - coords.y * math.sin(z_rot)),
        y=int(coords.x * math.sin(z_rot) + coords.y * math.cos(z_rot)),
        z=coords.z,
    )
    coords = Coordinate(
        x=int(coords.x * math.cos(y_rot) + coords.z * math.sin(y_rot)),
        y=coords.y,
        z=int(-coords.x * math.sin(y_rot) + coords.z * math.cos(y_rot)),
    )
    coords = Coordinate(
        x=coords.x,
        y=int(coords.y * math.cos(x_rot) - coords.z * math.sin(x_rot)),
        z=int(coords.y * math.sin(x_rot) + coords.z * math.cos(x_rot)),
    )
    return coords


def parse(input_str: str) -> Dict[int, ScannerReport]:
    scanner_reports: DefaultDict[int, ScannerReport] = defaultdict(
        lambda: ScannerReport()
    )
    scanner_number = 0
    for line in input_str.splitlines():
        line = line.strip()
        if not line:
            continue

        if m := re.match(r"--- scanner (\d+) ---", line):
            scanner_number = int(m.group(1))
        elif m := re.match(rf"({NUM}),({NUM}),({NUM})", line):
            scanner_report = scanner_reports[scanner_number]
            scanner_report.scanner_number = scanner_number
            scanner_report.add_reading(Coordinate(*(int(s) for s in m.groups())))
        else:
            raise ValueError(f"Cannot parse line '{line}'")

    return scanner_reports


def find_overlap(base: ScannerReport, report: ScannerReport) -> Optional[ScannerReport]:
    for rotated_report in report.rotations():
        for pt_1, pt_2 in itertools.product(base.readings, rotated_report.readings):
            offset = pt_1 - pt_2  # pt_2 relative to pt_1
            adjusted_positions = {coords + offset for coords in rotated_report.readings}
            intersections = set(base.readings) & adjusted_positions
            if len(intersections) >= 12:
                assert base.position is not None
                rotated_report.position = base.position + offset
                return rotated_report

    return None


def find_known_positions(data: Dict[int, ScannerReport]) -> Dict[int, ScannerReport]:
    # Mapping of relative location to scan 0 and the report that matches
    known_positions: Dict[int, ScannerReport] = {0: data.pop(0)}
    known_positions[0].position = Coordinate(0, 0, 0)

    no_overlap = []

    for it in range(len(data)):
        for first, second in itertools.product(
            list(known_positions.values()), list(data.values())
        ):
            if (first.scanner_number, second.scanner_number) in no_overlap:
                continue

            print(
                f"Looking for overlaps between {first.scanner_number} and {second.scanner_number}"
            )

            if overlap := find_overlap(first, second):
                print(f"    Found overlap: {overlap}")
                known_positions[overlap.scanner_number] = overlap
                data.pop(second.scanner_number)
                break
            else:
                no_overlap.append((first.scanner_number, second.scanner_number))
        print(f"iteration {it}")
    return known_positions


def calculate_part1(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    known_positions = find_known_positions(data)

    beacons = set()
    for scanner_report in known_positions.values():
        for beacon_pos in scanner_report.readings:
            assert scanner_report.position is not None
            beacons.add(scanner_report.position + beacon_pos)
    return len(beacons)


def calculate_part2(input_str: str) -> int:
    data = parse(input_str)  # noqa: F841
    known_positions = find_known_positions(data)

    max_distance = 0
    for first, second in itertools.combinations(known_positions.values(), 2):
        assert second.position is not None
        assert first.position is not None
        offset = second.position - first.position
        distance = sum(abs(d) for d in offset)
        max_distance = max(max_distance, distance)
    return max_distance


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        # print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()
