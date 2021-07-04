import os

import psycopg2

from fantasy_funball.helpers.mappers.scraper_to_postgres import (
    scraper_date_to_datetime_postgres,
    scraper_deadline_to_datetime_postgres,
    scraper_fixture_to_postgres,
)
from fantasy_funball.models import Fixture, Gameday, Gameweek
from fantasy_funball.scraping.fixture_scraper import FixtureScraper


def setup_fixtures():
    # Wipe postgres db fixture collection before adding setting up
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
        "truncate fantasy_funball_fixture, "
        "fantasy_funball_result,"
        "fantasy_funball_gameday,"
        "fantasy_funball_choices, "
        "fantasy_funball_gameweek;"
    )
    conn.commit()
    conn.close()

    # TODO: Refactor, v. messy
    fixture_scraper = FixtureScraper()
    gameweek_one = fixture_scraper.get_yearly_fixtures(until_week=1)[0]

    # Map retrieved weekly fixtures to Django model format
    deadline_postgres_format = scraper_deadline_to_datetime_postgres(
        date=gameweek_one["gameweek_1_deadline"]
    )
    gameweek = Gameweek(deadline=deadline_postgres_format)

    gameweek_one_fixtures = gameweek_one["gameweek_1_fixtures"]
    gameday_one = gameweek_one_fixtures[0]
    gameday_date_postgres_format = scraper_date_to_datetime_postgres(
        date=gameday_one["date"],
    )
    gameday = Gameday(
        date=gameday_date_postgres_format,
        gameweek=gameweek,
    )

    # save gameweek & gameday objects
    gameweek.save()
    gameday.save()

    for fixture in gameday_one["matches"]:
        fixture_postgres_format = scraper_fixture_to_postgres(
            data=fixture,
        )

        fixture = Fixture(
            home_team=fixture_postgres_format["home_team"],
            away_team=fixture_postgres_format["away_team"],
            kickoff=fixture_postgres_format["kickoff"],
            gameday=gameday,
        )

        fixture.save()


if __name__ == "__main__":
    setup_fixtures()
