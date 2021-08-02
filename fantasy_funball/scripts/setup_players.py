import os

import psycopg2

from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Player, Team


def setup_players() -> None:
    # Wipe postgres player table before adding setting up
    db_url = os.environ.get("DATABASE_URL")
    if db_url is not None:
        conn = psycopg2.connect(db_url, sslmode="require")
    else:
        postgres_creds = {
            "database": os.environ.get("DATABASE_NAME"),
            "host": os.environ.get("DATABASE_HOST"),
            "port": os.environ.get("DATABASE_PORT"),
            "user": os.environ.get("DATABASE_USER"),
            "password": os.environ.get("DATABASE_PASSWORD"),
        }

        conn = psycopg2.connect(**postgres_creds)

    cur = conn.cursor()
    cur.execute(
        "truncate fantasy_funball_player, "
        "fantasy_funball_result_assists,"
        "fantasy_funball_result_scorers,"
        "fantasy_funball_team,"
        "fantasy_funball_result,"
        "fantasy_funball_fixture,"
        "fantasy_funball_choices;"
    )
    conn.commit()
    conn.close()

    fpl_interface = FPLInterface()

    teams = fpl_interface.retrieve_teams()

    for team_name in teams.values():
        team_inst = Team(team_name=team_name)
        team_inst.save()

    players = fpl_interface.retrieve_players()

    for player in players:
        team_obj = Team.objects.get(team_name=player["team"])

        player_inst = Player(
            first_name=player["first_name"],
            surname=player["surname"],
            team=team_obj,
            position=player["position"],
        )

        player_inst.save()
