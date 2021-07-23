import json
from typing import Dict, List, Set

import django
import requests

django.setup()

from fantasy_funball.models import Player


class FPLInterface:
    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api"
        self.url = "https://fantasy.premierleague.com/api/bootstrap-static/"

    def retrieve_teams(self) -> Dict:
        request_response = requests.get(url=f"{self.base_url}/bootstrap-static/")
        raw_team_data = json.loads(request_response.content)["teams"]
        team_data = {team["id"]: team["name"] for team in raw_team_data}

        return team_data

    def retrieve_players(self) -> List[Dict]:
        request_response = requests.get(url=f"{self.base_url}/bootstrap-static/")
        raw_player_data = json.loads(request_response.content)["elements"]

        team_data = self.retrieve_teams()

        player_data = [
            {
                "id": player["id"],
                "first_name": player["first_name"],
                "surname": player["second_name"],
                "team": team_data[player["team"]],
            }
            for player in raw_player_data
        ]

        return player_data

    def retrieve_weekly_scorers(self, gameweek_no: int) -> Set[int]:
        """Get fantasy funball IDs of gameweek scorers"""
        request_response = requests.get(
            url=f"{self.base_url}/event/{gameweek_no}/live/"
        )
        raw_weekly_data = json.loads(request_response.content)

        all_player_data = self.retrieve_players()

        # Get the FPL API ID of each goal scorer for requested gameweek
        fpl_scorer_ids = set()
        for player_data in raw_weekly_data["elements"]:
            if player_data["stats"]["goals_scored"] > 0:
                fpl_scorer_ids.add(player_data["id"])

        # Get scorer info from retrieve_players()
        ff_scorer_ids = set()
        for id in fpl_scorer_ids:
            player_info = next(
                player for player in all_player_data if player["id"] == id
            )

            # Get fantasy_funball ID assigned to that player
            ff_player = Player.objects.get(
                first_name=player_info["first_name"],
                surname=player_info["surname"],
                team__team_name=player_info["team"],
            )

            ff_scorer_ids.add(ff_player.id)

        return ff_scorer_ids

    def retrieve_weekly_assists(self, gameweek_no: int) -> Set[int]:
        """Get fantasy funball IDs of gameweek assisters"""
        request_response = requests.get(
            url=f"{self.base_url}/event/{gameweek_no}/live/"
        )
        raw_weekly_data = json.loads(request_response.content)

        all_player_data = self.retrieve_players()

        # Get the FPL API ID of each assister for requested gameweek
        fpl_assist_ids = set()
        for player_data in raw_weekly_data["elements"]:
            if player_data["stats"]["assists"] > 0:
                fpl_assist_ids.add(player_data["id"])

        # Get assister info from retrieve_players()
        ff_assist_ids = set()
        for id in fpl_assist_ids:
            player_info = next(
                player for player in all_player_data if player["id"] == id
            )

            # Get fantasy_funball ID assigned to that player
            ff_player = Player.objects.get(
                first_name=player_info["first_name"],
                surname=player_info["surname"],
                team__team_name=player_info["team"],
            )

            ff_assist_ids.add(ff_player.id)

        return ff_assist_ids


if __name__ == "__main__":
    fpl_interface = FPLInterface()
    players = fpl_interface.retrieve_players()
    teams = fpl_interface.retrieve_teams()
