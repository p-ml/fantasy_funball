import json
from unittest import TestCase, skip

import requests
from rest_framework import status


class TestFunballer(TestCase):
    def setUp(self) -> None:
        self.funballer_url = (
            "http://0.0.0.0:8080/fantasy_funball/funballer/"
        )

    @skip("WIP")
    def test_retrieve_all_funballers(self):
        response = requests.get(url=self.funballer_url)
        response_content = json.loads(response.content)

        expected_output = [
            {
                "id": 21,
                "first_name": "Patrick",
                "surname": "McLaughlin",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "1050"
            },
            {
                "id": 22,
                "first_name": "Ben",
                "surname": "Webster",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "8251"
            },
            {
                "id": 23,
                "first_name": "Henry",
                "surname": "Crossman",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "5064"
            },
            {
                "id": 24,
                "first_name": "Will",
                "surname": "Cobbett",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "8285"
            },
            {
                "id": 25,
                "first_name": "Theo",
                "surname": "Adde",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "9306"
            },
            {
                "id": 26,
                "first_name": "Gordon",
                "surname": "Leeks",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "0625"
            },
            {
                "id": 27,
                "first_name": "Josh",
                "surname": "De La Haye",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "9839"
            },
            {
                "id": 28,
                "first_name": "Adam",
                "surname": "Hodgson",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "9308"
            },
            {
                "id": 29,
                "first_name": "Ilya",
                "surname": "Stolyarov",
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "0322"
            },
            {
                "id": 30,
                "first_name": "Steve",
                "surname": None,
                "player_points": 0,
                "team_points": 0,
                "points": 0,
                "pin": "2361"
            }
        ]

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, expected_output)
