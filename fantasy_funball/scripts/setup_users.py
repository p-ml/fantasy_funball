import os

import psycopg2

from fantasy_funball.models import Funballer


def setup_users() -> None:
    # Wipe postgres user collection before adding setting up
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
    cur.execute("truncate fantasy_funball_choices, fantasy_funball_funballer;")
    conn.commit()
    conn.close()

    people = [
        {
            "first_name": "Patrick",
            "surname": "McLaughlin",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
        },
        {
            "first_name": "Ben",
            "surname": "Webster",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
        },
        {
            "first_name": "Henry",
            "surname": "Crossman",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
        },
        {
            "first_name": "Will",
            "surname": "Cobbett",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
        },
    ]

    for person in people:
        funballer = Funballer(
            first_name=person["first_name"],
            surname=person["surname"],
            points=person["points"],
            player_points=person["player_points"],
            team_points=person["team_points"],
        )
        funballer.save()
