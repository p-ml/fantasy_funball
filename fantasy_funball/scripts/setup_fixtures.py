from pymongo import MongoClient

from fantasy_funball.helpers.mappers.scraper_to_mongo import (
    scraper_date_to_datetime_mongo,
    scraper_deadline_to_datetime_mongo,
    scraper_fixture_to_mongo,
)
from fantasy_funball.models import Fixture, Gameday, Gameweek
from fantasy_funball.scraping.get_fixtures import (
    get_yearly_fixtures,
)


def setup_fixtures():
    # Wipe mongo db fixture collection before adding setting up
    mongo_client = MongoClient("mongodb://localhost:27017")
    mongo_db = mongo_client.fantasy_funball_db
    mongo_db.fantasy_funball_fixture.drop()
    mongo_db.fantasy_funball_gameday.drop()
    mongo_db.fantasy_funball_gameweek.drop()

    # TODO: Refactor, v. messy
    gameweek_one = get_yearly_fixtures(until_week=1)[0]

    # Map retrieved weekly fixtures to Django model format
    deadline_mongo_format = scraper_deadline_to_datetime_mongo(
        date=gameweek_one["gameweek_1_deadline"]
    )
    gameweek = Gameweek(deadline=deadline_mongo_format)

    gameweek_one_fixtures = gameweek_one["gameweek_1_fixtures"]
    gameday_one = gameweek_one_fixtures[0]
    gameday_date_mongo_format = scraper_date_to_datetime_mongo(
        date=gameday_one["date"],
    )
    gameday = Gameday(
        date=gameday_date_mongo_format,
        gameweek=gameweek,
    )

    # save gameweek & gameday objects
    gameweek.save()
    gameday.save()

    for fixture in gameday_one["matches"]:
        fixture_mongo_format = scraper_fixture_to_mongo(
            data=fixture,
        )

        fixture = Fixture(
            home_team=fixture_mongo_format["home_team"],
            home_score=fixture_mongo_format["home_score"],
            away_team=fixture_mongo_format["away_team"],
            away_score=fixture_mongo_format["away_score"],
            gameday=gameday,
        )

        fixture.save()


if __name__ == "__main__":
    setup_fixtures()
