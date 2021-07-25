from unittest import TestCase
from unittest.mock import patch

import django
from django.test import Client
from rest_framework import status

django.setup()

from fantasy_funball.models import Team

PLAYER_VIEW_PATH = "fantasy_funball.views.player"


class TestPlayerViewSet(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @patch(f"{PLAYER_VIEW_PATH}.Result.objects.filter")
    @patch(f"{PLAYER_VIEW_PATH}.Player.objects.filter")
    def test_get(self, mock_retrieve_player, mock_retrieve_result):
        expected_output = [
            {
                "first_name": "Hugo",
                "surname": "Lloris",
                "team": 1,
                "id": 1,
            }
        ]

        mock_retrieve_result.return_value.count.return_value = 0

        mock_retrieve_player.return_value.values.return_value = expected_output

        response = self.client.get("/fantasy_funball/spurs/players/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_output)

    @patch(f"{PLAYER_VIEW_PATH}.Player.objects.filter")
    def test_get_team_not_found(self, mock_retrieve_player):
        mock_retrieve_player.side_effect = Team.DoesNotExist
        invalid_team_name = "barcelona"
        response = self.client.get(f"/fantasy_funball/{invalid_team_name}/players/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(str(response.data["detail"]), f"{invalid_team_name} not found")
