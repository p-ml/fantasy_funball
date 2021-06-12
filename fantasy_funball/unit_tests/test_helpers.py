from datetime import datetime
from unittest import TestCase

import pytz

from fantasy_funball.helpers.mappers.scraper_to_mongo import (
    scraper_date_to_datetime_mongo,
    scraper_deadline_to_datetime_mongo,
    scraper_fixture_to_mongo,
)


class TestScraperToMongo(TestCase):
    def setUp(self) -> None:
        self.mock_scraper_deadline = {
            "date": "Mon 1 Oct 10:00",
        }
        self.mock_scraper_date = "Monday 1 October 2021"
        self.mock_scraper_fixture = {
            "game": "Tottenham Hotspur 6:0 Arsenal",
        }

        self.timezone = pytz.timezone("Europe/London")

    def test_scraper_deadline_to_datetime_mongo(self):
        expected_output_no_tz = datetime(2021, 10, 1, 10, 0, 0)
        expected_output = self.timezone.localize(expected_output_no_tz)

        result = scraper_deadline_to_datetime_mongo(
            date=self.mock_scraper_deadline,
        )

        self.assertEqual(result, expected_output)

    def test_scraper_date_to_datetime_mongo(self):
        expected_output_no_tz = datetime(2021, 10, 1, 0, 0, 0)
        expected_output = self.timezone.localize(expected_output_no_tz)

        result = scraper_date_to_datetime_mongo(
            date=self.mock_scraper_date,
        )

        self.assertEqual(result, expected_output)

    def test_scraper_fixture_to_mongo(self):
        expected_output = {
            "home_team": "Tottenham Hotspur",
            "home_score": "6",
            "away_team": "Arsenal",
            "away_score": "0",
        }

        result = scraper_fixture_to_mongo(
            data=self.mock_scraper_fixture,
        )

        self.assertEqual(result, expected_output)
