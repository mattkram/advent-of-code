import os
import shutil
from datetime import date
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

SESSION_ID = os.environ["SESSION_ID"]

PROJECT_ROOT = Path(__file__).parent
TEMPLATE_DIR = PROJECT_ROOT / "template"


def make_path(year: int, day: Optional[int] = None) -> Path:
    path = Path(f"y{year}")
    if day is not None:
        path /= f"day{day:02d}"
    return path


def clone_template(day: date) -> None:
    destination = make_path(day.year, day.day)
    destination.mkdir(exist_ok=True, parents=True)
    for file in TEMPLATE_DIR.glob("*.py"):
        if not (destination / file.name).exists():
            shutil.copy2(file, destination)


def get_day() -> date:
    today = date.today()

    max_day = max(
        int(path.name.replace("day", "")) for path in make_path(today.year).glob("day*")
    )
    max_day = min(max_day, today.day) + 1
    return date(today.year, today.month, max_day)


def download_data(date_obj: date) -> None:
    destination = make_path(date_obj.year, date_obj.day) / "input.txt"
    if destination.exists():
        raise FileExistsError(f"File {destination} exists, skipping download")

    r = requests.get(
        f"https://adventofcode.com/{date_obj.year}/day/{date_obj.day}/input",
        cookies={"session": SESSION_ID},
    )
    r.raise_for_status()
    with destination.open("w") as fp:
        fp.write(r.text)


def main() -> None:
    date_obj = get_day()
    clone_template(date_obj)
    download_data(date_obj)


if __name__ == "__main__":
    main()
