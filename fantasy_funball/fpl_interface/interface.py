import json
from typing import Dict, List

import requests


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

    def retrieve_weekly_scorers(self):
        pass

    def retrieve_weekly_assists(self):
        pass


if __name__ == "__main__":
    fpl_interface = FPLInterface()
    players = fpl_interface.retrieve_players()
    teams = fpl_interface.retrieve_teams()
