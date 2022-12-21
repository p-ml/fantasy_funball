import json
from unittest import TestCase

import django
import requests
from rest_framework import status

django.setup()
from functional_tests.harness import FunctionalTestHarness


class TestGameweekView(TestCase):
    def setUp(self) -> None:
        self.harness = FunctionalTestHarness()

        self.dummy_fixture = self.harness.setup_dummy_fixture()
        self.gameweek_url = "http://0.0.0.0:8000/fantasy_funball/gameweek"

        self.gameweek_no = self.dummy_fixture.gameday.gameweek.gameweek_no
        self.gameday_id = self.dummy_fixture.gameday_id

    def tearDown(self) -> None:
        self.harness.teardown_dummy_fixture()

    def test_retrieve_gameweek_data(self):
        response = requests.get(f"{self.gameweek_url}/{self.gameweek_no}")

        expected_output = [
            {
                "id": self.gameday_id,
                "home_team__team_name": self.dummy_fixture.home_team.team_name,
                "away_team__team_name": self.dummy_fixture.away_team.team_name,
                "kickoff": self.dummy_fixture.kickoff,
                "gameday__date": "Sat 1 Jan 22",
            }
        ]
        response_content = json.loads(response.content)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, expected_output)

    def test_retrieve_gameweek_invalid_gameweek_id(self):
        bad_gameweek_id = self.gameweek_no + 99
        response = requests.get(f"{self.gameweek_url}/{bad_gameweek_id}")
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)
