from random import randrange

import django

django.setup()

from fantasy_funball.models import Player, Team


def get_random_team() -> Team:
    """Retrieve a random team from the database"""
    teams = list(Team.objects.all())

    team_index = randrange(0, len(teams))

    return teams[team_index]


def get_random_player() -> Player:
    """Retrieve a random midfielder/forward from the database"""
    # Get all midfielders & forwards
    players = list(
        Player.objects.filter(
            position__in={"Midfielder", "Forward"},
        )
    )

    player_index = randrange(0, len(players))

    return players[player_index]


if __name__ == "__main__":
    player = get_random_player()
    team = get_random_team()
