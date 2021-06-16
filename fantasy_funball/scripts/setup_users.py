import os

import psycopg2

from fantasy_funball.models import Funballer


def setup_users() -> None:
    # Wipe postgres user collection before adding setting up
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
            "points": 0,
        },
        {
            "first_name": "Ben",
            "surname": "Webster",
            "points": 0,
        },
        {
            "first_name": "Henry",
            "surname": "Crossman",
            "points": 0,
        },
        {
            "first_name": "Will",
            "surname": "Cobbett",
            "points": 0,
        },
    ]

    for person in people:
        funballer = Funballer(
            first_name=person["first_name"],
            surname=person["surname"],
            points=person["points"],
        )
        funballer.save()
