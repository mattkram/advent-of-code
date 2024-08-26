from pathlib import Path
from typing import Dict, List, NamedTuple, Set

import pytest

INPUTS_FILE = Path(__file__).parent / "input.txt"

ParsedInput = List["Food"]


class Food(NamedTuple):
    ingredients: Set[str]
    allergens: Set[str]


def parse(input_str: str) -> ParsedInput:
    data = []

    for line in input_str.strip().splitlines():
        ingredient_str, _, allergen_str = line.strip().partition("(contains ")

        food = Food(
            ingredients={s.strip() for s in ingredient_str.split()},
            allergens={s.strip() for s in allergen_str[:-1].split(",")},
        )
        data.append(food)
    return data


def calculate(foods: ParsedInput) -> str:
    allergen_options: Dict[str, Set[str]] = {}

    for food in foods:
        for allergen in food.allergens:
            if allergen not in allergen_options:
                allergen_options[allergen] = set(food.ingredients)
            else:
                allergen_options[allergen] &= food.ingredients

    allergen_map: Dict[str, str] = {}

    while any(allergen_options.values()):
        for allergen, options in allergen_options.items():
            if len(options) != 1:
                continue  # to next item
            allergen_map[allergen] = ingredient = list(options)[0]

            # Remove ingredient from all options
            for o in allergen_options.values():
                try:
                    o.remove(ingredient)
                except KeyError:
                    pass
    return ",".join(allergen_map[key] for key in sorted(allergen_map))


TEST_INPUTS = [
    (
        """
        mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
        trh fvjkl sbzzf mxmxvkd (contains dairy)
        sqjhc fvjkl (contains soy)
        sqjhc mxmxvkd sbzzf (contains fish)
        """,
        "mxmxvkd,sqjhc,fvjkl",
    )
]


@pytest.mark.parametrize("input_str,expected", TEST_INPUTS)
def test(input_str: str, expected: int) -> None:
    assert calculate(parse(input_str)) == expected


def main() -> str:
    with INPUTS_FILE.open() as fp:
        return calculate(parse(fp.read()))


if __name__ == "__main__":
    print(f"The answer is {main()}")
