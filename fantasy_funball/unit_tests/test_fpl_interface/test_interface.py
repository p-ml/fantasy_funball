from unittest import TestCase
from unittest.mock import Mock, patch

from requests import Response

from fantasy_funball.fpl_interface.interface import FPLInterface

FPL_INTERFACE_PATH = "fantasy_funball.fpl_interface.interface"


class TestFPLInterface(TestCase):
    def setUp(self) -> None:
        self.interface = FPLInterface()

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
            b' "assists": 0}]}'
        )
        mock_get_request.return_value = mock_response

        mock_retrieve_teams.return_value = {17: "Spurs"}

        expected_output = [
            {
                "id": 353,
                "first_name": "Hugo",
                "surname": "Lloris",
                "team": "Spurs",
                "goals": 0,
                "assists": 0,
            }
        ]

        output = self.interface.retrieve_players()

        self.assertEqual(output, expected_output)
