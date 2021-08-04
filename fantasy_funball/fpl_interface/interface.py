import json
from typing import Dict, List, Set

import django
import requests

django.setup()

from fantasy_funball.models import Fixture, Player, Team


class FPLInterface:
    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api"
        self.position_dict = {
            1: "Goalkeeper",
            2: "Defender",
            3: "Midfielder",
            4: "Forward",
        }

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
                "position": self.position_dict[player["element_type"]],
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

    def _determine_gameday_from_teams(self, home_team: str, away_team: str):
        # Check fixtures in db to get gameday_id
        gameday = Fixture.objects.get(
            home_team__team_name=home_team,
            away_team__team_name=away_team,
        )

        return gameday.gameday_id

    def retrieve_gameweek_results(self, gameweek_no: int) -> List[Dict]:
        """Check gameweek results"""
        request_response = requests.get(
            url=f"{self.base_url}/fixtures?event={gameweek_no}"
        )

        raw_gameweek_results = json.loads(request_response.content)
        team_ids = self.retrieve_teams()

        # Pull out finished games
        finished_games = [game for game in raw_gameweek_results if game["finished"]]

        gameweek_results = []
        for game in finished_games:
            # Get team name from id
            home_team_name = team_ids[game["team_h"]]
            away_team_name = team_ids[game["team_a"]]

            home_team = Team.objects.get(team_name=home_team_name)
            away_team = Team.objects.get(team_name=away_team_name)

            # Get gameday id using team names
            gameday_id = self._determine_gameday_from_teams(
                home_team=home_team_name,
                away_team=away_team_name,
            )

            formatted_result = {
                "home_team": home_team,
                "home_score": game["team_h_score"],
                "away_team": away_team,
                "away_score": game["team_a_score"],
                "gameday": gameday_id,
            }

            gameweek_results.append(formatted_result)

        return gameweek_results


if __name__ == "__main__":
    fpl_interface = FPLInterface()
    results = fpl_interface.retrieve_gameweek_results(gameweek_no=1)
