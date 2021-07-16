import os
from datetime import datetime, timezone

import psycopg2

from fantasy_funball.models import Gameday, Result, Team


def setup_results() -> None:
    # Wipe postgres result table before adding setting up
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

    conn.commit()
    conn.close()

    results = [
        {
            "home_team": "Spurs",
            "home_score": 10,
            "away_team": "Arsenal",
            "away_score": 0,
            "date": datetime.strptime(
                "2021-08-13 00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f"
            ).replace(tzinfo=timezone.utc),
        },
        {
            "home_team": "Chelsea",
            "home_score": 2,
            "away_team": "Brentford",
            "away_score": 8,
            "date": datetime.strptime(
                "2021-08-13 00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f"
            ).replace(tzinfo=timezone.utc),
        },
    ]

    for result in results:
        result_inst = Result(
            home_team=Team.objects.get(team_name=result["home_team"]),
            home_score=result["home_score"],
            away_team=Team.objects.get(team_name=result["away_team"]),
            away_score=result["away_score"],
            gameday=Gameday.objects.get(date=result["date"]),
        )
        result_inst.save()


if __name__ == "__main__":
    setup_results()
