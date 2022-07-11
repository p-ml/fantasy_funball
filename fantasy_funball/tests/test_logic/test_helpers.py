from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch

import pytz

from fantasy_funball.logic import determine_gameweek_no
from fantasy_funball.logic.helpers import get_teams_playing_in_gameweek
from fantasy_funball.models import Gameweek, Team

HELPERS_PATH = "fantasy_funball.logic.helpers"


class TestHelpers(TestCase):
    def setUp(self) -> None:
        self.first_mock_gameweek_obj = Mock(spec=Gameweek)
        self.second_mock_gameweek_obj = Mock(spec=Gameweek)

        self.first_mock_deadline = datetime(2021, 9, 1, 15, 0, 0, 0, pytz.UTC)
        self.second_mock_deadline = datetime(2021, 10, 1, 15, 0, 0, 0, pytz.UTC)

        self.first_mock_gameweek_obj.deadline = self.first_mock_deadline
        self.first_mock_gameweek_obj.gameweek_no = 1
        self.second_mock_gameweek_obj.deadline = self.second_mock_deadline
        self.second_mock_gameweek_obj.gameweek_no = 2

        self.mock_gameweeks = [
            self.first_mock_gameweek_obj,
            self.second_mock_gameweek_obj,
        ]

    @patch(f"{HELPERS_PATH}.datetime")
    @patch(f"{HELPERS_PATH}.list")
    def test_determine_gameweek_no(
        self,
        mock_gameweek_info_list,
        mock_datetime_now,
    ):
        # Datetime between two mock gameweek deadlines
        mock_current_time = datetime(2021, 9, 15, 15, 0, 0, 0)

        mock_gameweek_info_list.return_value = self.mock_gameweeks

        mock_datetime_now.now.return_value = mock_current_time

        output = determine_gameweek_no()

        self.assertEqual(output, 1)

    @patch(f"{HELPERS_PATH}.datetime")
    @patch(f"{HELPERS_PATH}.list")
    def test_determine_gameweek_no_pre_season(
        self,
        mock_gameweek_info_list,
        mock_datetime_now,
    ):
        # Datetime before both gameweek deadlines
        mock_current_time = datetime(2021, 8, 1, 15, 0, 0, 0)

        mock_gameweek_info_list.return_value = self.mock_gameweeks

        mock_datetime_now.now.return_value = mock_current_time

        output = determine_gameweek_no()
        self.assertEqual(output, 0)

    @patch(f"{HELPERS_PATH}.datetime")
    @patch(f"{HELPERS_PATH}.list")
    def test_determine_gameweek_no_post_season(
        self,
        mock_gameweek_info_list,
        mock_datetime_now,
    ):
        # Datetime after both gameweek deadlines
        mock_current_time = datetime(2021, 12, 1, 15, 0, 0, 0)

        mock_gameweek_info_list.return_value = self.mock_gameweeks

        mock_datetime_now.now.return_value = mock_current_time

        output = determine_gameweek_no()
        self.assertEqual(output, 2)

    @patch(f"{HELPERS_PATH}.Team.objects.all")
    @patch(f"{HELPERS_PATH}.Fixture.objects.filter")
    def test_get_teams_playing_in_gameweek(self, mock_fixtures, mock_teams):
        mock_fixtures.return_value.values.return_value = [
            {
                "home_team": 17,
                "away_team": 1,
            }
        ]

        mock_team_home = Mock(spec=Team)
        mock_team_home.team_name = "Spurs"

        mock_team_away = Mock(spec=Team)
        mock_team_away.team_name = "Arsenal"

        expected_output = [mock_team_home, mock_team_away]

        mock_teams.return_value.filter.return_value = expected_output

        output = get_teams_playing_in_gameweek(gameweek_no=1)  # arbitrary input

        mock_teams.return_value.filter.assert_called_once_with(id__in=[17, 1])

        self.assertEqual(output, expected_output)
