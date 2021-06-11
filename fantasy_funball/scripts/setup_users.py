from pymongo import MongoClient

from fantasy_funball.models import Funballer


def setup_users() -> None:
    # Wipe mongo db user collection before adding setting up
    mongo_client = MongoClient("mongodb://localhost:27017")
    mongo_db = mongo_client.fantasy_funball_db
    users_col = mongo_db.fantasy_funball_funballer
    users_col.drop()

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
