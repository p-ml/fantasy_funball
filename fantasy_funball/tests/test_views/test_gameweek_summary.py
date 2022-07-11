from unittest import TestCase
from unittest.mock import Mock, patch

from django.test import Client
from rest_framework import status

from fantasy_funball.models import GameweekSummary

GAMEWEEK_SUMMARY_VIEW_PATH = "fantasy_funball.views.gameweek_summary"


class GameweekSummaryView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.gameweek_summary_url = "/fantasy_funball/gameweek/summary/"
        self.dummy_gameweek_summary = [{"text": "Hello World"}]
        self.headers = {"content_type": "application/json"}

    @patch(f"{GAMEWEEK_SUMMARY_VIEW_PATH}.GameweekSummary.objects.all")
    def test_get_gameweek_summary(self, mock_retrieve_gameweek_summary):
        expected_output = self.dummy_gameweek_summary

        mock_retrieve_gameweek_summary.return_value.values.return_value = expected_output

        response = self.client.get(path=f"{self.gameweek_summary_url}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_output[0])

    @patch(f"{GAMEWEEK_SUMMARY_VIEW_PATH}.GameweekSummary")
    def test_put_gameweek_summary(self, mock_gameweek_summary):
        expected_output = self.dummy_gameweek_summary

        mock_gameweek_summary.objects.all.return_value.values.return_value = (
            expected_output
        )

        mock_new_gameweek_summary = Mock(spec=GameweekSummary)
        mock_new_gameweek_summary.text = self.dummy_gameweek_summary

        mock_gameweek_summary.return_value = mock_new_gameweek_summary

        response = self.client.put(
            path=f"{self.gameweek_summary_url}",
            data='{"text": "hello world"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
