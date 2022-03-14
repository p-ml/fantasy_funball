import json
from unittest import TestCase

import pytest
import requests
from rest_framework import status


@pytest.mark.django_db
class TestGameweekSummary(TestCase):
    def setUp(self) -> None:
        self.gameweek_summary = {"text": "Test Gameweek Summary"}
        self.gameweek_summary_url = (
            "http://0.0.0.0:8080/fantasy_funball/gameweek/summary/"
        )

    def test_gameweek_summary(self):
        # Test PUT gameweek summary
        response = requests.put(
            url=self.gameweek_summary_url,
            data=self.gameweek_summary,
        )

        self.assertTrue(response.status_code, status.HTTP_201_CREATED)

        # Test GET gameweek summary
        response = requests.get(
            url=self.gameweek_summary_url,
        )

        response_content = json.loads(response.content)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, self.gameweek_summary)
