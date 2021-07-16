import os

import psycopg2

from fantasy_funball.helpers.mappers.scraper_to_postgres import (
    scraper_date_to_datetime_postgres,
    scraper_deadline_to_datetime_postgres,
    scraper_fixture_to_postgres,
)
from fantasy_funball.models import Fixture, Gameday, Gameweek, Team
from fantasy_funball.scraping.fixture_scraper import FixtureScraper


def setup_fixtures():
    # Wipe postgres db fixture table before adding setting up
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
    gameweeks = fixture_scraper.get_yearly_fixtures(until_week=38)

    for gameweek_no, gameweek_data in enumerate(gameweeks):
        # Map retrieved weekly fixtures to Django model format
        deadline_postgres_format = scraper_deadline_to_datetime_postgres(
            date=gameweek_data["gameweek_deadline"]
        )
        gameweek = Gameweek(
            deadline=deadline_postgres_format,
            gameweek_no=gameweek_no + 1,  # enumerate() uses zero indexing
        )

        gameweek.save()

        gameweek_fixtures = gameweek_data["gameweek_fixtures"]
        gamedays = [gameday for gameday in gameweek_fixtures]

        for gameday_data in gamedays:
            gameday_date_postgres_format = scraper_date_to_datetime_postgres(
                date=gameday_data["date"],
            )
            gameday = Gameday(
                date=gameday_date_postgres_format,
                gameweek=gameweek,
            )

            gameday.save()

            for match_data in gameday_data["matches"]:
                fixture_postgres_format = scraper_fixture_to_postgres(
                    data=match_data,
                )

                fixture = Fixture(
                    home_team=Team.objects.get(
                        team_name=fixture_postgres_format["home_team"]
                    ),
                    away_team=Team.objects.get(
                        team_name=fixture_postgres_format["away_team"]
                    ),
                    kickoff=fixture_postgres_format["kickoff"],
                    gameday=gameday,
                )

                fixture.save()


if __name__ == "__main__":
    setup_fixtures()
