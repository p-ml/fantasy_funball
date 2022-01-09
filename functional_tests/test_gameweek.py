import json
from unittest import TestCase, skip

import requests
from rest_framework import status


class TestGameweekEndpoint(TestCase):
    def setUp(self) -> None:
        self.gameweek_id = 38
        self.gameweek_url = "http://0.0.0.0:8080/fantasy_funball/gameweek"

    @skip("WIP")
    def test_retrieve_gameweek_data(self):
        # TODO: Set up dummy data for FTs
        response = requests.get(f"{self.gameweek_url}/{self.gameweek_id}")

        expected_output = [
                {
                    "id": 531,
                    "home_team__team_name": "Arsenal",
                    "away_team__team_name": "Everton",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 532,
                    "home_team__team_name": "Brentford",
                    "away_team__team_name": "Leeds",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 533,
                    "home_team__team_name": "Brighton",
                    "away_team__team_name": "West Ham",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 534,
                    "home_team__team_name": "Burnley",
                    "away_team__team_name": "Newcastle",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 535,
                    "home_team__team_name": "Chelsea",
                    "away_team__team_name": "Watford",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 536,
                    "home_team__team_name": "Crystal Palace",
                    "away_team__team_name": "Man Utd",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 537,
                    "home_team__team_name": "Leicester",
                    "away_team__team_name": "Southampton",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 538,
                    "home_team__team_name": "Liverpool",
                    "away_team__team_name": "Wolves",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 539,
                    "home_team__team_name": "Man City",
                    "away_team__team_name": "Aston Villa",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                },
                {
                    "id": 540,
                    "home_team__team_name": "Norwich",
                    "away_team__team_name": "Spurs",
                    "kickoff": "2022-05-22 15:00:00",
                    "gameday__date": "Sun 22 May 22"
                }
        ]
        response_content = json.loads(response.content)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, expected_output)

    @skip("WIP")
    def test_retrieve_gameweek_invalid_gameweek_id(self):
        bad_gameweek_id = self.gameweek_id + 99
        response = requests.get(f"{self.gameweek_url}/{bad_gameweek_id}")
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)
