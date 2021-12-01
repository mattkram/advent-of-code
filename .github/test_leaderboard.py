import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Set

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
def members() -> Dict[int, Set[leaderboard.MemberScore]]:
    data = leaderboard.get_data_from_aoc()
    return leaderboard.get_leaderboard(data)


def test_members(members: List[leaderboard.MemberScore]) -> None:
    """Members are sorted first by descending local score, then descending stars."""
    assert members == {
        10: {
            leaderboard.MemberScore(name="Kirby O", local_score=10, stars=10),
            leaderboard.MemberScore(name="Matt K", local_score=8, stars=10),
        },
        8: {leaderboard.MemberScore(name="Jerry R", local_score=9, stars=8)},
        7: {leaderboard.MemberScore(name="Chip A", local_score=7, stars=7)},
        2: {leaderboard.MemberScore(name="Rivers C", local_score=3, stars=2)},
    }


@pytest.fixture()
def message_lines(members: Dict[int, Set[leaderboard.MemberScore]]) -> List[str]:
    return [s.rstrip() for s in leaderboard.format_leader_message(members).splitlines()]


def test_format_message(message_lines: List[str]) -> None:
    prefix_emoji = ":christmas_tree: :star: :santa::skin-tone-3:"
    suffix_emoji = ":mother_christmas::skin-tone-3: :star: :christmas_tree:"
    assert message_lines == [
        f"{prefix_emoji} Advent of Code Day 3 {suffix_emoji}",
        "",
        "Here is the current leaderboard:",
        "",
        ":trophy:    10 :star:",
        "    - Kirby O",
        "    - Matt K",
        ":second_place_medal:    8 :star:",
        "    - Jerry R",
        ":third_place_medal:    7 :star:",
        "    - Chip A",
        "2 :star:",
        "    - Rivers C",
        "",
        f"<{leaderboard.LEADERBOARD_URL}|View Leaderboard Online>",
        "",
        "Please avoid any spoilers in the main channel and place any daily solution "
        "chat in the thread below :point_down:",
    ]
