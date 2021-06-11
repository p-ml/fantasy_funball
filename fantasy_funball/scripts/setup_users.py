from fantasy_funball.models import Funballer


def setup_users() -> None:
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
