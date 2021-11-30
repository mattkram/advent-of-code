"""Grab the leaderboard from Advent of Code and post it to Slack.

Modified from the version found at: https://github.com/tomswartz07/AdventOfCodeLeaderboard

"""
import datetime
import os
import sys
from itertools import zip_longest
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple

import requests
from dotenv import load_dotenv

load_dotenv()

LEADERBOARD_ID = os.environ["LEADERBOARD_ID"]
SESSION_ID = os.environ["SESSION_ID"]
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

# You should not need to change this URL
LEADERBOARD_URL = "/".join(
    [
        "https://adventofcode.com",
        str(datetime.datetime.today().year),
        "leaderboard",
        "private",
        "view",
        str(LEADERBOARD_ID),
    ]
)


class MemberScore(NamedTuple):
    name: str
    local_score: int
    stars: int


def get_data_from_aoc() -> Dict[str, Any]:
    """Retrieve leaderboard data from Advent of Code website."""
    r = requests.get(f"{LEADERBOARD_URL}.json", cookies={"session": SESSION_ID})
    if r.status_code != requests.codes.ok:
        print("Error retrieving leaderboard")
        sys.exit(1)
    return r.json()


def get_leaderboard(data: Dict[str, Any]) -> List[MemberScore]:
    """Handle member lists from AoC leaderboard."""

    # get members from json
    members_json = data["members"]

    # get member name, score and stars
    members = [
        MemberScore(m["name"], m["local_score"], m["stars"])
        for m in members_json.values()
    ]

    # sort members by score, descending
    members.sort(key=lambda s: (s.local_score, s.stars), reverse=True)

    return members


def format_leader_message(members: List[MemberScore]) -> str:
    """Format the message to conform to Slack's API."""
    lines = []

    # add each member to message
    medals = [":trophy:", ":second_place_medal:", ":third_place_medal:"]
    for member, medal in zip_longest(members, medals, fillvalue=""):
        lines.append(
            f"{medal} *{member.name}* {member.local_score} Points, {member.stars} Stars".strip()
        )

    lines.append(f"\n<{LEADERBOARD_URL}|View Leaderboard Online>")

    return "\n".join(lines)


def post_message(message: str) -> None:
    """Post the message to to Slack's API in the proper channel."""
    payload = {
        "icon_emoji": ":christmas_tree:",
        "username": "advent of code leaderboard",
        "text": message,
    }
    requests.post(SLACK_WEBHOOK, json=payload)


def main() -> None:
    """Main program loop."""
    # Retrieve raw data from Advent of Code
    data = get_data_from_aoc()

    # Parse the raw data into a sorted list of members
    members = get_leaderboard(data)

    # generate message to send to slack
    message = format_leader_message(members)

    # send message to slack
    post_message(message)


if __name__ == "__main__":
    main()
