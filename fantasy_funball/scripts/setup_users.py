import os

import psycopg2

from fantasy_funball.models import Funballer
from fantasy_funball.scripts.db_connection import database_connection


def setup_users() -> None:
    # Wipe postgres user table before adding setting up
    conn = database_connection()

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
            "pin": "1050",
        },
        {
            "first_name": "Ben",
            "surname": "Webster",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "8251",
        },
        {
            "first_name": "Henry",
            "surname": "Crossman",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "5064",
        },
        {
            "first_name": "Will",
            "surname": "Cobbett",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "8285",
        },
        {
            "first_name": "Theo",
            "surname": "Adde",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "9306",
        },
        {
            "first_name": "Gordon",
            "surname": "Leeks",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "0625",
        },
        {
            "first_name": "Josh",
            "surname": "De La Haye",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "9839",
        },
        {
            "first_name": "Adam",
            "surname": "Hodgson",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "9308",
        },
        {
            "first_name": "Ilya",
            "surname": "Stolyarov",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "0322",
        },
        {
            "first_name": "Steve",
            "player_points": 0,
            "team_points": 0,
            "points": 0,
            "pin": "2361",
        },
    ]

    for person in people:
        funballer = Funballer(
            first_name=person["first_name"],
            surname=person.get("surname"),  # Is optional
            points=person["points"],
            player_points=person["player_points"],
            team_points=person["team_points"],
            pin=person["pin"],
        )
        funballer.save()
