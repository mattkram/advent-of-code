from pathlib import Path
from typing import List
from typing import Optional

import pytest


def load_input_lines() -> List[str]:
    """Load the input data, returning a list of lines."""
    input_file = Path(__file__).parent / "input.txt"
    with input_file.open() as ff:
        return ff.read().splitlines()


class OrbitalMap:
    def __init__(self, input_list: List[str]):
        self.planets = {"COM": Planet(name="COM")}

        self.load_input(input_list)

    def load_input(self, input_list: List[str]) -> None:
        # Map children to parent strings (children are unique, parents are not)
        parent_map = {}
        for line in input_list:
            parent_name, child_name = line.split(")")
            parent_map[child_name] = parent_name

        # Create all planet objects and store in dictionary
        for child_name, parent_name in parent_map.items():
            self.planets[child_name] = Planet(name=child_name)

        # Assign parent objectss using name in mapping
        for child_name, parent_name in parent_map.items():
            self.planets[child_name].parent = self.planets[parent_name]

        for p in self.planets.values():
            print(f"{p}: num_orbits = {p.num_orbits}")

    @property
    def total_num_orbits(self) -> int:
        return sum(p.num_orbits for p in self.planets.values())

    def get_num_transfers(self, name_1: str, name_2: str) -> int:
        ancestors_1 = self.planets[name_1].ancestors
        ancestors_2 = self.planets[name_2].ancestors

        # Find last common ancestor
        last_common = None
        for a in ancestors_1:
            if a in ancestors_2:
                last_common = a
                break
        assert last_common is not None

        return ancestors_1.index(last_common) + ancestors_2.index(last_common)


class Planet:
    def __init__(self, name: str):
        self.name = name
        self.parent: Optional["Planet"] = None

    def __repr__(self) -> str:
        return f"Planet(name='{self.name}')"

    @property
    def num_orbits(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.num_orbits + 1

    @property
    def ancestors(self) -> List["Planet"]:
        if self.parent is None:
            return []
        return [self.parent] + self.parent.ancestors


def calculate(input_lines: List[str]) -> int:
    m = OrbitalMap(input_lines)
    return m.total_num_orbits


@pytest.mark.parametrize(
    "input_lines,expected",
    [
        (["COM)B"], 1),
        (["COM)B", "COM)C"], 2),
        (["COM)B", "COM)C", "C)D"], 4),
        (["COM)B", "B)C", "C)D", "D)E", "E)F"], 15),
        (
            [
                "COM)B",
                "B)C",
                "C)D",
                "D)E",
                "E)F",
                "B)G",
                "G)H",
                "D)I",
                "E)J",
                "J)K",
                "K)L",
            ],
            42,
        ),
    ],
)
def test_compare_results(input_lines: List[str], expected: bool) -> None:
    assert calculate(input_lines) == expected


def test_compare_final_answer() -> None:
    assert main() == 247_089


def main() -> int:
    lines = load_input_lines()
    answer = calculate(lines)
    print(f"The answer is: {answer}")
    return answer


if __name__ == "__main__":
    main()
