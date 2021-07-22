from unittest import TestCase
from unittest.mock import patch

import django
from django.test import Client
from rest_framework import status

django.setup()

from fantasy_funball.models import Choices

FUNBALLER_VIEW_PATH = "fantasy_funball.views.funballer"


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
        response = self.client.get("/fantasy_funball/funballer/choices/tony")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.exception)
        self.assertEqual(
            str(response.data["detail"]),
            f"Choices for {invalid_funballer_name} not found",
        )

    def test_post_update_existing_choice(self):
        pass

    def test_post_new_choice(self):
        pass
