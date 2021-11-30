# Advent of Code

This repo contains my solutions to the [Advent of Code](https://adventofcode.com) challenge.

## Setup
The dependencies are managed with `poetry`.
To install, type

```poetry install```

I'm using `pre-commit` for code quality checks.
Install the pre-commit hooks with

```pre-commit install```

## Daily Process

Each year, day, and part has its own module, e.g. `y2020.day01.part1`.
Each file can either be run as a main module or as a `pytest` test file.

Start by copying the template to a specific day:

```
cp template y2020/day01
```

While developing the solution, the tests can be run with:

```
poetry run pytest y2020/day01/part1.py
```

To print the final answer, use:

```
poetry run python -m y2020.day01.part
```

or

```
poetry run python y2020/day01/part01.py
```
