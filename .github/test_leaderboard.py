import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

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

    def mocked_get_contest_day() -> int:
        return 3

    monkeypatch.setattr(leaderboard, "get_data_from_aoc", mocked_get_data_from_aoc)
    monkeypatch.setattr(leaderboard, "post_message", mocked_post_message)
    monkeypatch.setattr(leaderboard, "get_contest_day", mocked_get_contest_day)


def test_leaderboard() -> None:
    """Smoke test."""
    leaderboard.main()


@pytest.fixture()
def members() -> List[leaderboard.MemberScore]:
    data = leaderboard.get_data_from_aoc()
    return leaderboard.get_leaderboard(data)


def test_members(members: List[leaderboard.MemberScore]) -> None:
    """Members are sorted first by descending local score, then descending stars."""
    assert members == [
        leaderboard.MemberScore(name="Kirby O", local_score=10, stars=10),
        leaderboard.MemberScore(name="Matt K", local_score=10, stars=9),
        leaderboard.MemberScore(name="Jerry R", local_score=9, stars=8),
        leaderboard.MemberScore(name="Chip A", local_score=7, stars=7),
    ]


@pytest.fixture()
def message_lines(members: List[leaderboard.MemberScore]) -> List[str]:
    return [s.strip() for s in leaderboard.format_leader_message(members).splitlines()]


def test_format_message(message_lines: List[str]) -> None:
    assert message_lines == [
        "It is day 3 of Advent of Code! Here is the current leaderboard:",
        "",
        ":trophy: *Kirby O* 10 Points, 10 Stars",
        ":second_place_medal: *Matt K* 10 Points, 9 Stars",
        ":third_place_medal: *Jerry R* 9 Points, 8 Stars",
        "*Chip A* 7 Points, 7 Stars",
        "",
        f"<{leaderboard.LEADERBOARD_URL}|View Leaderboard Online>",
    ]
