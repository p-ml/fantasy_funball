from random import randrange
from typing import List

import django

django.setup()

from fantasy_funball.models import Player, Team


def get_random_team(non_permitted_teams: List[Team] = None) -> Team:
    """Retrieve a random team from the database"""
    if non_permitted_teams is None:
        non_permitted_teams = []

    all_teams = list(Team.objects.all())

    permitted_teams = [team for team in all_teams if team not in non_permitted_teams]

    team_index = randrange(0, len(permitted_teams))

    return permitted_teams[team_index]


def get_random_player(non_permitted_players: List[Player] = None) -> Player:
    """Retrieve a random midfielder/forward from the database"""
    # Get all midfielders & forwards
    if non_permitted_players is None:
        non_permitted_players = []

    all_players = list(
        Player.objects.filter(
            position__in={"Midfielder", "Forward"},
        )
    )

    permitted_players = [
        player for player in all_players if player not in non_permitted_players
    ]

    player_index = randrange(0, len(permitted_players))

    return permitted_players[player_index]


if __name__ == "__main__":
    player = get_random_player()
    team = get_random_team()
