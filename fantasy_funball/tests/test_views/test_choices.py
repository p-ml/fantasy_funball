from unittest import TestCase
from unittest.mock import Mock, patch

from django.test import Client
from rest_framework import status

from fantasy_funball.models import Choices, Funballer, Gameweek, Player, Team

CHOICES_VIEW_PATH = "fantasy_funball.views.choices"


class FunballerChoiceView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.base_url = "/fantasy_funball/funballer/choices"
        self.funballer_name = "patrick"

    @patch(f"{CHOICES_VIEW_PATH}.Choices.objects.filter")
    def test_get(self, mock_retrieve_choices):
        expected_output = [
            {
                "funballer_id__first_name": self.funballer_name,
                "gameweek_id__gameweek_no": 1,
                "team_choice__team_name": "Spurs",
                "player_choice__first_name": "Hugo",
                "player_choice__surname": "Lloris",
            }
        ]

        mock_retrieve_choices.return_value.values.return_value = expected_output

        response = self.client.get(f"{self.base_url}/{self.funballer_name}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_output)

    @patch(f"{CHOICES_VIEW_PATH}.Choices.objects.filter")
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

    @patch(f"{CHOICES_VIEW_PATH}.team_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.player_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{CHOICES_VIEW_PATH}.Player.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Team.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Choices")
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

        mock_funballer = Mock(spec=Funballer)
        mock_funballer.first_name = "Mock"

        mock_retrieve_funballer.return_value = mock_funballer
        mock_retrieve_team.return_value = {}
        mock_retrieve_player.return_value = {}
        mock_check_for_passed_deadline.return_value = {}

        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        response = self.client.post(
            path=f"{self.base_url}/submit/0000",
            data={
                "gameweek_no": 1,
                "team_choice": "Tottenham Hotspur",
                "player_choice": "3739",
                "deadline_passed_check": True,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data), "Choice updated")

    @patch(f"{CHOICES_VIEW_PATH}.team_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.player_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{CHOICES_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Team.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Choices.objects.get")
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

        mock_funballer = Mock(spec=Funballer)
        mock_funballer.first_name = "Mock"

        mock_retrieve_funballer.return_value = mock_funballer
        mock_check_for_passed_deadline.return_value = {}
        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        mock_retrieve_team.side_effect = Team.DoesNotExist

        response = self.client.post(
            path=f"{self.base_url}/submit/0000",
            data={
                "gameweek_no": 1,
                "team_choice": invalid_team_choice,
                "player_choice": "3739",
                "deadline_passed_check": True,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(
            str(response.data["detail"]),
            f"Team with name {invalid_team_choice} not found",
        )

    @patch(f"{CHOICES_VIEW_PATH}.team_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.player_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{CHOICES_VIEW_PATH}.Player.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Team.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Choices.objects.get")
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
        invalid_player_choice = "9999999"

        mock_gameweek_obj = Mock(spec=Gameweek)
        mock_gameweek_obj.deadline = "mock date goes here"
        mock_retrieve_gameweek.return_value = mock_gameweek_obj

        mock_retrieve_choices.return_value = {}

        mock_funballer = Mock(spec=Funballer)
        mock_funballer.first_name = "Mock"

        mock_retrieve_funballer.return_value = mock_funballer
        mock_retrieve_team.return_value = {}
        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        mock_retrieve_player.side_effect = Player.DoesNotExist
        mock_check_for_passed_deadline.return_value = {}

        response = self.client.post(
            path=f"{self.base_url}/submit/0000",
            data={
                "gameweek_no": 1,
                "team_choice": "Barcelona",
                "player_choice": invalid_player_choice,
                "deadline_passed_check": True,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(
            str(response.data["detail"]),
            f"Player with id {invalid_player_choice} not found",
        )

    @patch(f"{CHOICES_VIEW_PATH}.team_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.player_selection_check")
    @patch(f"{CHOICES_VIEW_PATH}.check_for_passed_deadline")
    @patch(f"{CHOICES_VIEW_PATH}.Player.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Gameweek.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Funballer.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Team.objects.get")
    @patch(f"{CHOICES_VIEW_PATH}.Choices")
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

        mock_funballer = Mock(spec=Funballer)
        mock_funballer.first_name = "Mock"

        mock_team = Mock(spec=Team)
        mock_team.team_name = "Spurs"

        mock_player = Mock(spec=Player)
        mock_player.first_name = "First Name"
        mock_player.surname = "Surname"

        mock_retrieve_funballer.return_value = mock_funballer
        mock_retrieve_team.return_value = mock_team
        mock_retrieve_player.return_value = mock_player
        mock_check_for_passed_deadline.return_value = {}

        mock_player_selection_check.return_value = None
        mock_team_selection_check.return_value = None

        response = self.client.post(
            path=f"{self.base_url}/submit/0000",
            data={
                "gameweek_no": 1,
                "team_choice": "Tottenham Hotspur",
                "player_choice": "3739",
                "deadline_passed_check": True,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(response.data), "Choice submitted")

    @patch(f"{CHOICES_VIEW_PATH}.Team.objects.all")
    @patch(f"{CHOICES_VIEW_PATH}.Choices.objects.filter")
    def test_get_remaining_team_choices(
        self,
        mock_choices,
        mock_teams,
    ):
        mock_choices.return_value.values.return_value = [
            {"team_choice__team_name": "Spurs"},
            {"team_choice__team_name": "Spurs"},
            {"team_choice__team_name": "Brentford"},
        ]

        mock_teams.return_value.values.return_value = [
            {"team_name": "Spurs"},
            {"team_name": "Brentford"},
            {"team_name": "Liverpool"},
            {"team_name": "Gameweek Void"},
        ]

        expected_output = [
            {
                "team_name": "Spurs",
                "remaining_selections": 0,
            },
            {
                "team_name": "Brentford",
                "remaining_selections": 1,
            },
            {
                "team_name": "Liverpool",
                "remaining_selections": 2,
            },
        ]

        response = self.client.get(
            path=f"{self.base_url}/valid_teams/{self.funballer_name}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_output)

    @patch(f"{CHOICES_VIEW_PATH}.Choices.objects.filter")
    def test_get_remaining_team_choices_choices_not_found(
        self,
        mock_choices,
    ):
        mock_choices.DoesNotExist = BaseException
        mock_choices.side_effect = Choices.DoesNotExist

        response = self.client.get(
            path=f"{self.base_url}/valid_teams/{self.funballer_name}"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(
            str(response.data["detail"]),
            f"Choices for {self.funballer_name} not found",
        )
