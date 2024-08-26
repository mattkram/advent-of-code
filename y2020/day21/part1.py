import itertools
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


def calculate(foods: ParsedInput) -> int:
    allergen_options: Dict[str, Set[str]] = {}

    for food in foods:
        for allergen in food.allergens:
            if allergen not in allergen_options:
                allergen_options[allergen] = set(food.ingredients)
            else:
                allergen_options[allergen] &= food.ingredients

    all_ingredients = set(
        itertools.chain.from_iterable(food.ingredients for food in foods)
    )

    ingredients_with_potential_allergens = set(
        itertools.chain.from_iterable(allergen_options.values())
    )
    ingredients_without_allergens = (
        all_ingredients ^ ingredients_with_potential_allergens
    )

    return sum(
        ingredient in ingredients_without_allergens
        for food in foods
        for ingredient in food.ingredients
    )  # for food in foods_without_allergens for options in allergen_options.values())


TEST_INPUTS = [
    (
        """
        mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
        trh fvjkl sbzzf mxmxvkd (contains dairy)
        sqjhc fvjkl (contains soy)
        sqjhc mxmxvkd sbzzf (contains fish)
        """,
        5,
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
