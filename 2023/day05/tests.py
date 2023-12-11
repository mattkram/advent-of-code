from pathlib import Path

import pytest

from .solution import apply_maps_to_range
from .solution import calculate

TEST_INPUT = """
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
"""

INPUTS_FILE = Path(__file__).parent / "input.txt"
with INPUTS_FILE.open("r") as fp:
    REAL_INPUT = fp.read()


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 35, id="test-input"),
        pytest.param(REAL_INPUT, 261668924, id="real-data"),
    ],
)
def test_part1(input_str: str, expected: int) -> None:
    assert calculate(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        pytest.param(TEST_INPUT, 46, id="test-input"),
        pytest.param(REAL_INPUT, 24261545, id="real-data"),
    ],
)
def test_part2(input_str: str, expected: int) -> None:
    assert calculate(input_str, ranges=True) == expected


@pytest.mark.parametrize(
    "rng, expected_result",
    [
        pytest.param((0, 49), {(0, 49)}, id="no-overlap"),
        pytest.param((55, 74), {(57, 76)}, id="map-overlaps_range"),
        pytest.param((55, 85), {(57, 77), (76, 85)}, id="partial-overlap-left"),
        pytest.param((40, 70), {(40, 49), (52, 72)}, id="partial-overlap-right"),
        pytest.param((40, 85), {(40, 49), (52, 77), (76, 85)}, id="range-overlaps-map"),
    ],
)
def test_apply_maps_to_range(rng, expected_result):
    maps = [
        (50, 98, 2),  # {98 - 99}, -48
        (52, 50, 26),  # {50 - 75}, +2
    ]
    result = apply_maps_to_range(rng, maps)
    assert result == expected_result
