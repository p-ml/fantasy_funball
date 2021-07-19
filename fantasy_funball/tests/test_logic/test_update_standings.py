from unittest import TestCase

import django

from fantasy_funball.logic.update_standings import determine_gameweek_winners

django.setup()

from fantasy_funball.models import Result, Team


class TestUpdateStandings(TestCase):
    def setUp(self) -> None:
        self.mock_teams = [
            Team(team_name="Spurs"),
            Team(team_name="Arsenal"),
            Team(team_name="Brentford"),
            Team(team_name="Aston Villa"),
            Team(team_name="Chelsea"),
            Team(team_name="Liverpool"),
        ]

        self.mock_results = [
            Result(
                home_team=self.mock_teams[0],
                away_team=self.mock_teams[1],
                home_score=5,
                away_score=0,
            ),
            Result(
                home_team=self.mock_teams[2],
                away_team=self.mock_teams[3],
                home_score=2,
                away_score=4,
            ),
            Result(
                home_team=self.mock_teams[4],
                away_team=self.mock_teams[5],
                home_score=0,
                away_score=0,
            ),
        ]

    def test_determine_gameweek_winners(self):
        output = determine_gameweek_winners(
            gameweek_results=self.mock_results,
        )

        expected_output = [
            self.mock_teams[0],
            self.mock_teams[3],
        ]

        self.assertEqual(output, expected_output)
