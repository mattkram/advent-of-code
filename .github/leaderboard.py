"""Grab the leaderboard from Advent of Code and post it to Slack.

Modified from the version found at: https://github.com/tomswartz07/AdventOfCodeLeaderboard

"""
import datetime
import os
import sys
from collections import defaultdict
from itertools import zip_longest
from typing import Any
from typing import DefaultDict
from typing import Dict
from typing import NamedTuple
from typing import Set

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


def get_leaderboard(data: Dict[str, Any]) -> Dict[int, Set[MemberScore]]:
    """Handle member lists from AoC leaderboard."""

    # get members from json
    members_json = data["members"]

    # group members by total number of stars
    result: DefaultDict[int, Set[MemberScore]] = defaultdict(set)

    for value in members_json.values():
        member = MemberScore(value["name"], value["local_score"], value["stars"])
        result[member.stars].add(member)

    return result


def get_contest_day() -> int:
    today = datetime.datetime.today()
    delta = today - datetime.datetime(today.year, 12, 1)
    return delta.days + 1


def format_leader_message(members: Dict[int, Set[MemberScore]]) -> str:
    """Format the message to conform to Slack's API."""
    lines = []

    day = get_contest_day()
    if day < 1:
        lines.append("The contest hasn't started yet.")
    else:
        lines.append(
            " ".join(
                [
                    ":christmas_tree:",
                    ":star:",
                    ":santa::skin-tone-3:",
                    f"Advent of Code Day {day}",
                    ":mother_christmas::skin-tone-3:",
                    ":star:",
                    ":christmas_tree:",
                ]
            )
        )

    lines.append("\nHere is the current leaderboard:\n")

    # add each member to message
    medals = [":trophy:", ":second_place_medal:", ":third_place_medal:"]

    # sort members by score, descending
    sorted_star_sets = sorted(members.keys(), reverse=True)
    for num_stars, medal in zip_longest(sorted_star_sets, medals, fillvalue=""):
        members_with_stars = members[num_stars]
        if not members_with_stars or num_stars == 0:
            continue

        if medal:
            lines.append(f"{medal}    {num_stars} :star:")
        else:
            lines.append(f"{num_stars} :star:")

        for member in sorted(members_with_stars):
            lines.append(f"    - {member.name}")

    lines.append(f"\n<{LEADERBOARD_URL}|View Leaderboard Online>")

    lines.append(
        "\nPlease avoid any spoilers in the main channel and "
        "place any daily solution chat in the thread below :point_down:"
    )

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
