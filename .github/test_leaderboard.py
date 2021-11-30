import json
from pathlib import Path
from typing import Any
from typing import Dict

import leaderboard
import pytest


@pytest.fixture(autouse=True)
def mocked_data(monkeypatch: Any) -> None:
    def mocked_get_data_from_aoc() -> Dict[str, Any]:
        data_file = Path(__file__).parent / "test_data.json"
        with data_file.open("r") as fp:
            return json.load(fp)

    def mocked_post_message(message: str) -> None:
        return None

    monkeypatch.setattr(leaderboard, "get_data_from_aoc", mocked_get_data_from_aoc)
    monkeypatch.setattr(leaderboard, "post_message", mocked_post_message)


def test_leaderboard() -> None:
    leaderboard.main()
    assert False
