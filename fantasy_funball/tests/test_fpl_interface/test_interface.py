import json
from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch

import pytz
from requests import Response

from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Gameday, Player, Team
from fantasy_funball.tests.test_logic.mock_gameweek_live_data import (
    mock_gameweek_live_data,
)

FPL_INTERFACE_PATH = "fantasy_funball.fpl_interface.interface"


class TestFPLInterface(TestCase):
    def setUp(self) -> None:
        self.interface = FPLInterface()
        self.mock_gameweek_live_data = mock_gameweek_live_data()

    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_teams(self, mock_get_request):
        mock_response = Mock(spec=Response)
        mock_response.content = (
            b'{"teams": [{"code": 6, "draw": 0, "form": null, '
            b'"id": 17, "loss": 0, "name": "Spurs", "played": 0, '
            b'"points": 0, "position": 0, "short_name":"TOT", '
            b'"strength": 4, "team_division": null, "unavailable": false, '
            b'"win": 0, "strength_overall_home": 1190,'
            b'"strength_overall_away": 1250, "strength_attack_home": 1130, '
            b'"strength_attack_away": 1170, "strength_defence_home": 1250, '
            b'"strength_defence_away": 1290, "pulse_id": 21}]}'
        )
        mock_get_request.return_value = mock_response

        expected_output = {17: "Spurs"}

        output = self.interface.retrieve_teams()

        self.assertEqual(output, expected_output)

    @patch(f"{FPL_INTERFACE_PATH}.FPLInterface.retrieve_teams")
    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_players(self, mock_get_request, mock_retrieve_teams):
        mock_response = Mock(spec=Response)
        mock_response.content = (
            b'{"elements": [{"first_name": "Hugo", "id": 353,'
            b' "second_name": "Lloris", "team": 17, "goals_scored": 0,'
            b' "assists": 0, "element_type": 1}]}'
        )
        mock_get_request.return_value = mock_response

        mock_retrieve_teams.return_value = {17: "Spurs"}

        expected_output = [
            {
                "id": 353,
                "first_name": "Hugo",
                "surname": "Lloris",
                "team": "Spurs",
                "position": "Goalkeeper",
            }
        ]

        output = self.interface.retrieve_players()

        self.assertEqual(output, expected_output)

    @patch(f"{FPL_INTERFACE_PATH}.Player.objects.get")
    @patch(f"{FPL_INTERFACE_PATH}.FPLInterface.retrieve_players")
    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_weekly_scorers(
        self,
        mock_get_request,
        mock_retrieve_players,
        mock_get_player,
    ):
        mock_player = Mock(spec=Player)
        mock_player.id = 1234
        mock_get_player.return_value = mock_player

        mock_retrieve_players.return_value = [
            {
                "id": 390,
                "first_name": "Heung-Min",
                "surname": "Son",
                "team": "Spurs",
            }
        ]
        mock_get_response = Mock(spec=Response)

        # Convert dict from mock data to byte string
        mock_get_response.content = json.dumps(self.mock_gameweek_live_data).encode(
            "utf-8"
        )
        mock_get_request.return_value = mock_get_response

        output = self.interface.retrieve_weekly_scorers(gameweek_no=1)
        self.assertEqual(output, {1234})

    @patch(f"{FPL_INTERFACE_PATH}.Player.objects.get")
    @patch(f"{FPL_INTERFACE_PATH}.FPLInterface.retrieve_players")
    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_weekly_assists(
        self,
        mock_get_request,
        mock_retrieve_players,
        mock_get_player,
    ):
        mock_player = Mock(spec=Player)
        mock_player.id = 4321
        mock_get_player.return_value = mock_player

        mock_retrieve_players.return_value = [
            {
                "id": 390,
                "first_name": "Heung-Min",
                "surname": "Son",
                "team": "Spurs",
            }
        ]
        mock_get_response = Mock(spec=Response)

        # Convert dict from mock data to byte string
        mock_get_response.content = json.dumps(self.mock_gameweek_live_data).encode(
            "utf-8"
        )
        mock_get_request.return_value = mock_get_response

        output = self.interface.retrieve_weekly_assists(gameweek_no=1)
        self.assertEqual(output, {4321})

    @patch(f"{FPL_INTERFACE_PATH}.FPLInterface._determine_gameday_from_teams")
    @patch(f"{FPL_INTERFACE_PATH}.Team.objects.get")
    @patch(f"{FPL_INTERFACE_PATH}.FPLInterface.retrieve_teams")
    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_gameweek_results(
        self,
        mock_get_request,
        mock_retrieve_teams,
        mock_get_team,
        mock_determine_gameday_from_teams,
    ):
        mock_get_response = Mock(spec=Response)
        mock_get_response.content = json.dumps(
            [
                {
                    "finished": True,
                    "kickoff_time": "2021-08-13T19:00:00Z",
                    "team_a": 17,
                    "team_a_score": 10,
                    "team_h": 1,
                    "team_h_score": 0,
                }
            ]
        ).encode("utf-8")
        mock_get_request.return_value = mock_get_response

        mock_retrieve_teams.return_value = {1: "Arsenal", 17: "Spurs"}

        mock_team = Mock(spec=Team)
        mock_get_team.return_value = mock_team

        mock_determine_gameday_from_teams.return_value = 3

        expected_output = [
            {
                "home_team": mock_team,
                "home_score": 0,
                "away_team": mock_team,
                "away_score": 10,
                "gameday": 3,
            }
        ]

        output = self.interface.retrieve_gameweek_results(gameweek_no=1)

        self.assertEqual(expected_output, output)

    @patch(f"{FPL_INTERFACE_PATH}.Gameday.objects.get")
    @patch(f"{FPL_INTERFACE_PATH}.Team.objects.get")
    @patch(f"{FPL_INTERFACE_PATH}.FPLInterface.retrieve_teams")
    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_fixtures(
        self,
        mock_get_request,
        mock_retrieve_teams,
        mock_get_team,
        mock_get_gameday,
    ):
        mock_get_response = Mock(spec=Response)
        mock_get_response.content = json.dumps(
            [
                {
                    "finished": False,
                    "kickoff_time": "2021-08-13T19:00:00Z",
                    "team_a": 17,
                    "team_h": 1,
                }
            ]
        ).encode("utf-8")
        mock_get_request.return_value = mock_get_response

        mock_retrieve_teams.return_value = {1: "Arsenal", 17: "Spurs"}

        mock_team = Mock(spec=Team)
        mock_get_team.return_value = mock_team

        mock_gameday = Mock(spec=Gameday)
        mock_get_gameday.return_value = mock_gameday

        kickoff_datetime = datetime.strptime(
            "2021-08-13T19:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
        )

        expected_output = [
            {
                "home_team": mock_team,
                "away_team": mock_team,
                "kickoff": kickoff_datetime,
                "gameday": mock_gameday,
            }
        ]

        output = self.interface.retrieve_gameweek_fixtures(gameweek_no=1)

        self.assertEqual(output, expected_output)

    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_gameweek_deadline(
        self,
        mock_get_request,
    ):
        mock_get_response = Mock(spec=Response)
        mock_get_response.content = json.dumps(
            {
                "events": [
                    {
                        "deadline_time": "2021-08-13T19:00:00Z",
                    }
                ]
            }
        ).encode("utf-8")
        mock_get_request.return_value = mock_get_response

        output = self.interface.retrieve_gameweek_deadline(gameweek_no=1)

        expected_output = datetime(year=2021, month=8, day=13, hour=19, tzinfo=pytz.UTC)

        self.assertEqual(output, expected_output)

    @patch(f"{FPL_INTERFACE_PATH}.requests.get")
    def test_retrieve_gameday_dates(
        self,
        mock_get_request,
    ):
        mock_get_response = Mock(spec=Response)
        mock_get_response.content = json.dumps(
            [
                {
                    "kickoff_time": "2021-08-13T19:00:00Z",
                }
            ]
        ).encode("utf-8")
        mock_get_request.return_value = mock_get_response

        output = self.interface.retrieve_gameday_dates(gameweek_no=1)

        expected_output = {datetime(year=2021, month=8, day=13, tzinfo=pytz.UTC)}

        self.assertEqual(output, expected_output)
