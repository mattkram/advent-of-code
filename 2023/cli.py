import os
import shutil
from pathlib import Path

import requests
import typer
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

SESSION_COOKIE = os.environ.get("SESSION_COOKIE")
ROOT_DIR = Path.cwd()
while not (TEMPLATE_DIR := ROOT_DIR / "template").exists():
    ROOT_DIR = ROOT_DIR.parent

app = typer.Typer(add_completion=False, help="Welcome to the Anaconda CLI!")
console = Console()


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main() -> None:
    """Anaconda CLI."""


@app.command()
def get(day: int = typer.Option()) -> None:
    """Get data for a certain day."""
    year = 2023
    day_dir = Path(ROOT_DIR, str(year), f"day{day:02}")
    input_file = day_dir / "input.txt"
    input_file.parent.mkdir(parents=True, exist_ok=True)

    for f in TEMPLATE_DIR.glob("*"):
        dst = day_dir / f.name
        if not dst.exists():
            console.print(f"Copying from [cyan]{f}[/cyan] to [cyan]{dst}[/cyan]")
            shutil.copyfile(f, dst)
        else:
            console.print(f"Destination file [cyan]{dst}[/cyan] already exists.")

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
