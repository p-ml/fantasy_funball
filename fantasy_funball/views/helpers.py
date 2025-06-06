from datetime import datetime

import pytz

from core.exceptions import (
    GameweekDeadlinePassedError,
    PlayerSelectedTooManyTimes,
    TeamSelectedTooManyTimes,
)
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


def player_selection_check(funballer_first_name: str, player_id: int):
    """Checks that funballer has not already selected player"""
    # Get all players selected by funballer
    player_selections = Choices.objects.filter(
        funballer__first_name=funballer_first_name,
    ).values(
        "player_choice__first_name",
        "player_choice__surname",
        "player_choice_id",
    )

    # Extract player names
    player_ids = [player["player_choice_id"] for player in player_selections]

    selected_player_name_count = player_ids.count(player_id)

    if selected_player_name_count >= 1:
        # Get player name by id
        player = next(
            player
            for player in player_selections
            if player["player_choice_id"] == player_id
        )
        player_name = (
            f"{player['player_choice__first_name']} {player['player_choice__surname']}"
        )

        raise PlayerSelectedTooManyTimes(
            f"{funballer_first_name} has selected {player_name} more than once"
        )
