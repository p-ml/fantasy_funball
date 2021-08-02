from unittest import TestCase
from unittest.mock import Mock, patch

import django
from django.test import Client
from rest_framework import status

django.setup()

from fantasy_funball.models import Choices, Gameweek, Player, Team

FUNBALLER_VIEW_PATH = "fantasy_funball.views.choices"


class FunballerChoiceView(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @patch(f"{FUNBALLER_VIEW_PATH}.Choices.objects.filter")
    def test_get(self, mock_retrieve_choices):
        expected_output = [
            {
                "funballer_id__first_name": "Patrick",
                "gameweek_id__gameweek_no": 1,
                "team_choice__team_name": "Spurs",
                "player_choice__first_name": "Hugo",
                "player_choice__surname": "Lloris",
            }
        ]

        mock_retrieve_choices.return_value.values.return_value = expected_output

        response = self.client.get("/fantasy_funball/funballer/choices/patrick")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_output)

    @patch(f"{FUNBALLER_VIEW_PATH}.Choices.objects.filter")
    def test_get_choice_not_found(self, mock_retrieve_choices):
        mock_retrieve_choices.side_effect = Choices.DoesNotExist
        invalid_funballer_name = "tony"
        response = self.client.get(
            f"/fantasy_funball/funballer/choices/{invalid_funballer_name}"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(
            str(response.data["detail"]),
            f"Choices for {invalid_funballer_name} not found",
        )

    @patch(f"{FUNBALLER_VIEW_PATH}.team_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.player_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{FUNBALLER_VIEW_PATH}.Player.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Team.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Choices")
    def test_post_update_existing_choice(
        self,
        mock_choice,
        mock_retrieve_team,
        mock_retrieve_funballer,
        mock_retrieve_gameweek,
        mock_retrieve_player,
        mock_check_for_passed_deadline,
        mock_player_selection_check,
        mock_team_selection_check,
    ):
        mock_gameweek_obj = Mock(spec=Gameweek)
        mock_gameweek_obj.deadline = "mock date goes here"
        mock_retrieve_gameweek.return_value = mock_gameweek_obj

        mock_choice.objects.get.return_value = Mock(spec=Choices)
        mock_choice.return_value.save = {}
        mock_retrieve_funballer.return_value = {}
        mock_retrieve_team.return_value = {}
        mock_retrieve_player.return_value = {}
        mock_check_for_passed_deadline.return_value = {}

        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        response = self.client.post(
            path="/fantasy_funball/funballer/choices/patrick",
            data={
                "gameweek_no": 1,
                "team_choice": "Tottenham Hotspur",
                "player_choice": "Hugo Lloris",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data), "Choice updated")

    @patch(f"{FUNBALLER_VIEW_PATH}.team_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.player_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{FUNBALLER_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Team.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Choices.objects.get")
    def test_post_update_existing_choice_team_not_found(
        self,
        mock_retrieve_choices,
        mock_retrieve_team,
        mock_retrieve_funballer,
        mock_retrieve_gameweek,
        mock_check_for_passed_deadline,
        mock_player_selection_check,
        mock_team_selection_check,
    ):
        invalid_team_choice = "Barcelona"

        mock_gameweek_obj = Mock(spec=Gameweek)
        mock_gameweek_obj.deadline = "mock date goes here"
        mock_retrieve_gameweek.return_value = mock_gameweek_obj

        mock_retrieve_choices.return_value = {}
        mock_retrieve_funballer.return_value = {}
        mock_check_for_passed_deadline.return_value = {}
        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        mock_retrieve_team.side_effect = Team.DoesNotExist

        response = self.client.post(
            path="/fantasy_funball/funballer/choices/patrick",
            data={
                "gameweek_no": 1,
                "team_choice": invalid_team_choice,
                "player_choice": "",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(
            str(response.data["detail"]),
            f"Team with name {invalid_team_choice} not found",
        )

    @patch(f"{FUNBALLER_VIEW_PATH}.team_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.player_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{FUNBALLER_VIEW_PATH}.Player.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Team.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Choices.objects.get")
    def test_post_update_existing_choice_player_not_found(
        self,
        mock_retrieve_choices,
        mock_retrieve_team,
        mock_retrieve_funballer,
        mock_retrieve_gameweek,
        mock_retrieve_player,
        mock_check_for_passed_deadline,
        mock_player_selection_check,
        mock_team_selection_check,
    ):
        invalid_player_choice = "Lionel Messi"

        mock_gameweek_obj = Mock(spec=Gameweek)
        mock_gameweek_obj.deadline = "mock date goes here"
        mock_retrieve_gameweek.return_value = mock_gameweek_obj

        mock_retrieve_choices.return_value = {}
        mock_retrieve_funballer.return_value = {}
        mock_retrieve_team.return_value = {}
        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        mock_retrieve_player.side_effect = Player.DoesNotExist
        mock_check_for_passed_deadline.return_value = {}

        response = self.client.post(
            path="/fantasy_funball/funballer/choices/patrick",
            data={
                "gameweek_no": 1,
                "team_choice": "Barcelona",
                "player_choice": invalid_player_choice,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(
            str(response.data["detail"]),
            f"Player with name {invalid_player_choice} not found",
        )

    @patch(f"{FUNBALLER_VIEW_PATH}.team_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.player_selection_check")
    @patch(f"{FUNBALLER_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{FUNBALLER_VIEW_PATH}.Player.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Team.objects.get")
    @patch(f"{FUNBALLER_VIEW_PATH}.Choices")
    def test_post_new_choice(
        self,
        mock_choices,
        mock_retrieve_team,
        mock_retrieve_funballer,
        mock_retrieve_gameweek,
        mock_retrieve_player,
        mock_check_for_passed_deadline,
        mock_player_selection_check,
        mock_team_selection_check,
    ):
        mock_gameweek_obj = Mock(spec=Gameweek)
        mock_gameweek_obj.deadline = "mock date goes here"
        mock_retrieve_gameweek.return_value = mock_gameweek_obj

        mock_choices.DoesNotExist = BaseException
        mock_choices.objects.get.side_effect = Choices.DoesNotExist

        mock_choices.return_value = Mock(spec=Choices)
        mock_choices.save = {}

        mock_retrieve_funballer.return_value = {}
        mock_retrieve_team.return_value = {}
        mock_retrieve_player.return_value = {}
        mock_check_for_passed_deadline.return_value = {}

        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        response = self.client.post(
            path="/fantasy_funball/funballer/choices/patrick",
            data={
                "gameweek_no": 1,
                "team_choice": "Tottenham Hotspur",
                "player_choice": "Hugo Lloris",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(response.data), "Choice submitted")
