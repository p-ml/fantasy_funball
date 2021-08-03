from datetime import datetime

import django
import pytz

from core.exceptions import (
    GameweekDeadlinePassedError,
    PlayerSelectedTooManyTimes,
    TeamSelectedTooManyTimes,
)

django.setup()

from fantasy_funball.models import Choices


def check_for_passed_deadline(gameweek_deadline: datetime):
    """Raise an error if chosen gameweek deadline has already passed"""
    # Get current utc time
    current_time = datetime.now()
    utc = pytz.UTC
    current_time = utc.localize(current_time)

    if current_time > gameweek_deadline:
        raise GameweekDeadlinePassedError(
            "Choice cannot be updated/submitted once a gameweek deadline has passed"
        )


def team_selection_check(funballer_first_name: str, team_name: str):
    """Checks that funballer has not already selected team twice"""
    # Get all teams selected by funballer
    team_selections = Choices.objects.filter(
        funballer__first_name=funballer_first_name,
    ).values("team_choice__team_name")

    # Extract team names
    team_names = [team["team_choice__team_name"] for team in team_selections]

    selected_team_name_count = team_names.count(team_name)

    if selected_team_name_count >= 2:
        raise TeamSelectedTooManyTimes(
            f"{funballer_first_name} has selected {team_name} more than twice"
        )


def player_selection_check(funballer_first_name: str, player_name: str):
    """Checks that funballer has not already selected player"""
    # Get all players selected by funballer
    player_selections = Choices.objects.filter(
        funballer__first_name=funballer_first_name,
    ).values("player_choice__first_name", "player_choice__surname")

    # Extract player names
    player_names = [
        f"{player['player_choice__first_name']} {player['player_choice__surname']}"
        for player in player_selections
    ]

    selected_player_name_count = player_names.count(player_name)

    if selected_player_name_count >= 1:
        raise PlayerSelectedTooManyTimes(
            f"{funballer_first_name} has selected {player_name} more than once"
        )


if __name__ == "__main__":
    team_selection_check(funballer_first_name="Patrick", team_name="Spurs")
    player_selection_check(funballer_first_name="Patrick", player_name="Hugo Lloris")
