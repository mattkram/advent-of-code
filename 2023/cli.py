import os
from pathlib import Path

import requests
import typer
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

SESSION_COOKIE = os.environ.get("SESSION_COOKIE")


app = typer.Typer(add_completion=False, help="Welcome to the Anaconda CLI!")
console = Console()


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main() -> None:
    """Anaconda CLI."""


@app.command()
def get(day: int = typer.Option()) -> None:
    """Get data for a certain day."""
    year = 2023
    input_file = Path(f"day{day:02}", "input.txt")
    input_file.parent.mkdir(parents=True, exist_ok=True)

    if input_file.exists():
        console.print(f"Data file [cyan]{input_file}[/cyan] exists, skipping request")
        raise typer.Abort()

    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": SESSION_COOKIE},
    )
    assert response.status_code == 200
    content = response.text
    with input_file.open("w") as fp:
        fp.write(content)


if __name__ == "__main__":
    app()
