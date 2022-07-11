from unittest import TestCase
from unittest.mock import Mock, patch

from fantasy_funball.logic.standings import (
    ScorerAssistIds,
    determine_gameweek_winners,
    get_gameweek_results,
    get_weekly_assists,
    get_weekly_scorers,
    get_weekly_scorers_and_assists,
    get_weekly_team_picks,
)
from fantasy_funball.models import Assists, Choices, Goals, Result, Team

UPDATE_STANDINGS_PATH = "fantasy_funball.logic.standings"


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

    @patch(f"{UPDATE_STANDINGS_PATH}.determine_gameweek_winners")
    @patch(f"{UPDATE_STANDINGS_PATH}.Result.objects.filter")
    def test_get_gameweek_results(
        self,
        mock_retrieve_results,
        mock_determine_gameweek_winners,
    ):
        mock_retrieve_results.return_value = [self.mock_results[0]]

        mock_determine_gameweek_winners.return_value = self.mock_teams[0]

        response = get_gameweek_results(gameweek_no=1)

        self.assertEqual(response, self.mock_teams[0])

    @patch(f"{UPDATE_STANDINGS_PATH}.Choices.objects.filter")
    def test_get_weekly_team_picks(
        self,
        mock_retrieve_choices,
    ):
        mock_choice = Mock(spec=Choices)
        mock_choice.has_been_processed = False
        mock_choice.funballer_id = 1
        mock_choice.gameweek_id = 2
        mock_choice.player_choice_id = 10
        mock_choice.team_choice_id = 20

        mock_retrieve_choices.return_value = [mock_choice]

        response = get_weekly_team_picks(gameweek_no=1)

        self.assertEqual(response, [mock_choice])

    @patch(f"{UPDATE_STANDINGS_PATH}.list")
    def test_get_weekly_scorers(self, mock_list):
        mock_goal = Mock(spec=Goals)
        mock_goal.player_id = 123

        mock_list.return_value = [mock_goal]
        mock_result = Mock(spec=Result)
        mock_result.id = 1

        response = get_weekly_scorers(weekly_result_data=[mock_result])

        self.assertEqual(response, {123})

    @patch(f"{UPDATE_STANDINGS_PATH}.list")
    def test_get_weekly_assists(self, mock_list):
        mock_assist = Mock(spec=Assists)
        mock_assist.player_id = 321

        mock_list.return_value = [mock_assist]
        mock_result = Mock(spec=Result)
        mock_result.id = 2

        response = get_weekly_assists(weekly_result_data=[mock_result])

        self.assertEqual(response, {321})

    @patch(f"{UPDATE_STANDINGS_PATH}.get_weekly_assists")
    @patch(f"{UPDATE_STANDINGS_PATH}.get_weekly_scorers")
    @patch(f"{UPDATE_STANDINGS_PATH}.list")
    @patch(f"{UPDATE_STANDINGS_PATH}.Result.objects.filter")
    def test_get_weekly_scorers_and_assists(
        self,
        mock_retrieve_result,
        mock_convert_queryset,
        mock_get_weekly_scorers,
        mock_get_weekly_assists,
    ):
        mock_result = Mock(spec=Result)
        mock_retrieve_result.return_value = mock_result

        mock_convert_queryset.return_value = [mock_result]

        mock_get_weekly_scorers.return_value = {123}
        mock_get_weekly_assists.return_value = {321}

        output = get_weekly_scorers_and_assists(gameweek_no=1)

        self.assertIsInstance(output, ScorerAssistIds)
        self.assertEqual(output.scorer_ids, {123})
        self.assertEqual(output.assist_ids, {321})
