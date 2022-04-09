from datetime import datetime
from typing import List

import django
import pytz

django.setup()

from fantasy_funball.models import Fixture, Gameweek, Team


def get_teams_playing_in_gameweek(gameweek_no: int) -> List[Team]:
    """Retrieve a list of teams which played in the given gameweek"""
    # Get ids of teams in gameweek
    team_ids_in_gameweek = Fixture.objects.filter(
        gameday__gameweek__gameweek_no=gameweek_no
    ).values("home_team", "away_team")

    all_team_ids = []
    for fixture in list(team_ids_in_gameweek):
        all_team_ids.extend((fixture["home_team"], fixture["away_team"]))
    all_teams = list(Team.objects.all().filter(id__in=all_team_ids))

    return all_teams


def determine_gameweek_no() -> int:
    """Uses local time to determine what gameweek number we are in"""
    # Retrieve list of gameweek objects, sorted by deadline
    gameweek_info = list(Gameweek.objects.order_by("deadline"))

    # Get current datetime
    current_datetime_tz_unaware = datetime.now()
    utc = pytz.timezone("UTC")
    current_datetime = utc.localize(current_datetime_tz_unaware)

    gameweek_no = 0  # Season hasn't started yet
    for gameweek in gameweek_info:
        if current_datetime > gameweek.deadline:
            gameweek_no = gameweek.gameweek_no

    return gameweek_no


if __name__ == "__main__":
    get_teams_playing_in_gameweek(gameweek_no=32)
