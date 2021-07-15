import os

import psycopg2

from fantasy_funball.models import Choices, Funballer, Gameweek
from fantasy_funball.models.players import Player
from fantasy_funball.models.teams import Team


def setup_choices() -> None:
    # Wipe postgres choices table before adding setting up
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
    cur.execute("truncate fantasy_funball_choices;")
    conn.commit()
    conn.close()

    funballer = Funballer.objects.get(first_name="Patrick")
    gameweek_one = Gameweek.objects.get(gameweek_no=1)

    player_one = Player.objects.get(
        first_name="Hugo",
        surname="Lloris",
        team_id__team_name="Spurs",
    )
    player_two = Player.objects.get(
        first_name="Tanguy",
        surname="Ndombele",
        team_id__team_name="Spurs",
    )

    player_one.save()
    player_two.save()

    team_one = Team.objects.get(team_name="Spurs")

    choices = [
        {
            "funballer_id": funballer,
            "gameweek_id": gameweek_one,
            "team_choice": team_one,
            "player_choice": player_one,
        },
    ]

    for choice in choices:
        choice = Choices(
            funballer_id=choice["funballer_id"],
            gameweek_id=choice["gameweek_id"],
            team_choice=choice["team_choice"],
            player_choice=choice["player_choice"],
        )
        choice.save()
