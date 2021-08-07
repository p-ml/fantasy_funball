from random import randrange, shuffle
from typing import List

import django

django.setup()

from fantasy_funball.models import Choices, Funballer, Gameweek, Player, Team


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


def generate_steve_choices():
    """
    Generates Steve's picks for the season. Currently a fairly crude
    implementation, room for improvement/more clever choices
    """
    all_teams = list(Team.objects.all())
    all_players = list(
        Player.objects.filter(
            position__in={"Midfielder", "Forward"},
        )
    )

    # Duplicate teams (each team can be selected twice per season)
    all_teams.extend(all_teams)

    shuffle(all_teams)
    shuffle(all_players)

    steve = Funballer.objects.get(first_name="Steve")

    # Create a choice for each gameweek (starts at 1 for zero indexing)
    for i in range(1, 39):
        gameweek = Gameweek.objects.get(gameweek_no=i)
        choice = Choices(
            funballer=steve,
            gameweek=gameweek,
            team_choice=all_teams[i],
            player_choice=all_players[i],
        )
        choice.save()


if __name__ == "__main__":
    player = get_random_player()
    team = get_random_team()

    generate_steve_choices()
