import json
from unittest import TestCase

import django
import requests
from rest_framework import status

django.setup()
from functional_tests.harness import FunctionalTestHarness


class TestFunballerView(TestCase):
    def setUp(self) -> None:
        self.funballer_url = "http://0.0.0.0:8000/fantasy_funball/funballer/"
        self.dummy_funballer_data = {
            "first_name": "functional",
            "surname": "test",
            "points": 100,
            "team_points": 80,
            "player_points": 25,
            "pin": "4567",
        }

    def tearDown(self) -> None:
        harness = FunctionalTestHarness()
        harness.delete_funballer()

    def _post_funballer(self, funballer_data):
        post_response = requests.post(
            url=self.funballer_url,
            json=funballer_data,
        )

        post_response_content = json.loads(post_response.content)
        funballer_id = post_response_content.pop("id")

        self.assertTrue(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_response_content, funballer_data)

        return funballer_id

    def test_post_funballer(self):
        self._post_funballer(
            funballer_data=self.dummy_funballer_data,
        )

    def test_get_single_funballer(self):
        # First post a funballer
        funballer_id = self._post_funballer(
            funballer_data=self.dummy_funballer_data,
        )

        # Then, get that funballer
        get_response = requests.get(url=f"{self.funballer_url}{funballer_id}")
        get_response_content = json.loads(get_response.content)
        get_response_content.pop("id")

        self.assertTrue(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_content, self.dummy_funballer_data)

    def test_get_single_funballer_invalid_id(self):
        # Get single funballer, invalid id
        invalid_funballer_id = 999
        get_response_invalid_id = requests.get(
            url=f"{self.funballer_url}{invalid_funballer_id}"
        )
        get_response_invalid_id_content = json.loads(get_response_invalid_id.content)

        self.assertTrue(get_response_invalid_id.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            get_response_invalid_id_content["detail"],
            f"Funballer with id {invalid_funballer_id} not found",
        )

    def test_retrieve_all_funballers(self):
        # Post a funballer
        self._post_funballer(
            funballer_data=self.dummy_funballer_data,
        )

        # Then post a second
        second_funballer_data = {
            "first_name": "functional",
            "surname": "test",
            "points": 50,
            "team_points": 20,
            "player_points": 30,
            "pin": "6543",
        }
        self._post_funballer(
            funballer_data=second_funballer_data,
        )

        # Then, retrieve both funballers
        get_all_response = requests.get(url=self.funballer_url)
        get_all_response_content = json.loads(get_all_response.content)

        self.assertTrue(get_all_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_all_response_content), 2)

        # Remove ids for comparison
        for funballer in get_all_response_content:
            funballer.pop("id")

        expected_response = [
            self.dummy_funballer_data,
            second_funballer_data,
        ]

        self.assertEqual(get_all_response_content, expected_response)
