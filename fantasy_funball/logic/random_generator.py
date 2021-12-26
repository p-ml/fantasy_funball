from random import randrange, shuffle
from typing import List

import django

django.setup()

from fantasy_funball.models import Choices, Fixture, Funballer, Gameweek, Player, Team


def get_random_team(
    gameweek_no: int,
    non_permitted_teams: List[Team] = None,
) -> Team:
    """
    Retrieve a random team from the database; takes into account teams playing in
    the given gameweek, and excludes teams which have already been chosen twice.
    """
    if non_permitted_teams is None:
        non_permitted_teams = []

    # Get ids of teams in gameweek
    team_ids_in_gameweek = list(
        Fixture.objects.filter(gameday__gameweek__gameweek_no=gameweek_no).values(
            "home_team", "away_team"
        )
    )

    all_team_ids = []
    for fixture in team_ids_in_gameweek:
        all_team_ids.extend((fixture["home_team"], fixture["away_team"]))
    all_teams = list(Team.objects.all().filter(id__in=all_team_ids))

    # Do not allow "void" team to be selected
    void_team = Team.objects.get(team_name="Gameweek Void")
    non_permitted_teams.append(void_team)

    permitted_teams = [team for team in all_teams if team not in non_permitted_teams]

    team_index = randrange(0, len(permitted_teams))

    return permitted_teams[team_index]


def get_random_player(non_permitted_players: List[Player] = None) -> Player:
    """Retrieve a random midfielder/forward from the database"""
    if non_permitted_players is None:
        non_permitted_players = []

    # Get all midfielders & forwards
    all_players = list(
        Player.objects.filter(
            position__in={"Midfielder", "Forward"},
        )
    )

    # No need to not allow void player, as only selects midfielders/forwards
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
    get_random_team(
        gameweek_no=18,
    )
