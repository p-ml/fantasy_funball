import json
from unittest import TestCase

import requests
from rest_framework import status


class TestGameweekEndpoint(TestCase):
    def setUp(self) -> None:
        self.gameweek_id = 1
        self.gameweek_url = "http://localhost:8001/fantasy_funball/gameweek"

    def test_retrieve_gameweek_data(self):
        response = requests.get(f"{self.gameweek_url}/{self.gameweek_id}")

        expected_output = [
            {
                "away_team": "Arsenal",
                "gameday_id": 1,
                "home_team": "Brentford",
                "id": 1,
                "kickoff": "19:00",
            }
        ]
        response_content = json.loads(response.content)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, expected_output)

    def test_retrieve_gameweek_invalid_gameweek_id(self):
        bad_gameweek_id = self.gameweek_id + 99
        response = requests.get(f"{self.gameweek_url}/{bad_gameweek_id}")
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)
