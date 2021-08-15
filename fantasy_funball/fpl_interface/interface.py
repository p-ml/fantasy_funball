import json
from datetime import datetime
from typing import Dict, List, Set

import django
import pytz
import requests

django.setup()

from fantasy_funball.models import Fixture, Gameday, Player, Team


class FPLInterface:
    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api"
        self.position_dict = {
            1: "Goalkeeper",
            2: "Defender",
            3: "Midfielder",
            4: "Forward",
        }

        self.timezone = pytz.timezone("UTC")

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

    def _generate_team_scorer_assist_structure(self) -> Dict:
        """Generates a dictionary of sets, to store each team's
        scorers & assisters"""
        teams = self.retrieve_teams()
        team_names = list(teams.values())
        team_scorer_assist_structure = {team_name: {} for team_name in team_names}

        return team_scorer_assist_structure

    def retrieve_weekly_scorers(self, gameweek_no: int) -> Dict:
        """Get fantasy funball IDs of gameweek scorers"""
        request_response = requests.get(
            url=f"{self.base_url}/event/{gameweek_no}/live/"
        )
        raw_weekly_data = json.loads(request_response.content)

        all_player_data = self.retrieve_players()

        # Get the FPL API ID of each goal scorer for requested gameweek
        fpl_scorer_ids = {}
        for player_data in raw_weekly_data["elements"]:
            if player_data["stats"]["goals_scored"] > 0:
                fpl_scorer_ids[player_data["id"]] = (
                    player_data["stats"]["goals_scored"]
                )

        # Get scorer info from retrieve_players()
        team_scorer_structure = self._generate_team_scorer_assist_structure()
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

            team_scorer_structure[player_info["team"]][ff_player.id] = (
                fpl_scorer_ids[id]
            )

        return team_scorer_structure

    def retrieve_weekly_assists(self, gameweek_no: int) -> Dict:
        """Get fantasy funball IDs of gameweek assisters"""
        request_response = requests.get(
            url=f"{self.base_url}/event/{gameweek_no}/live/"
        )
        raw_weekly_data = json.loads(request_response.content)

        all_player_data = self.retrieve_players()

        # Get the FPL API ID of each assister for requested gameweek
        fpl_assist_ids = {}
        for player_data in raw_weekly_data["elements"]:
            if player_data["stats"]["assists"] > 0:
                fpl_assist_ids[player_data["id"]] = (
                    player_data["stats"]["assists"]
                )

        # Get assister info from retrieve_players()
        team_assist_structure = self._generate_team_scorer_assist_structure()
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

            team_assist_structure[player_info["team"]][ff_player.id] = (
                fpl_assist_ids[id]
            )

        return team_assist_structure

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

    def retrieve_gameweek_fixtures(self, gameweek_no: int) -> List[Dict]:
        """Get gameweek fixtures"""
        request_response = requests.get(
            url=f"{self.base_url}/fixtures?event={gameweek_no}"
        )

        raw_gameweek_data = json.loads(request_response.content)
        team_ids = self.retrieve_teams()

        # Pull out fixtures
        fixtures = [game for game in raw_gameweek_data if not game["finished"]]

        gameweek_fixtures = []
        for game in fixtures:
            # Get team name from id
            home_team_name = team_ids[game["team_h"]]
            away_team_name = team_ids[game["team_a"]]

            home_team = Team.objects.get(team_name=home_team_name)
            away_team = Team.objects.get(team_name=away_team_name)

            # Convert kickoff_time to date obj, strip off H:M:S
            kickoff_time = datetime.strptime(game["kickoff_time"], "%Y-%m-%dT%H:%M:%SZ")
            kickoff_date = kickoff_time.date()

            # Add back H:M:S, set to midnight
            date_unaware = datetime.combine(kickoff_date, datetime.min.time())

            date_aware = self.timezone.localize(date_unaware)

            gameday = Gameday.objects.get(date=date_aware)

            formatted_fixture = {
                "home_team": home_team,
                "away_team": away_team,
                "kickoff": kickoff_time,
                "gameday": gameday,
            }

            gameweek_fixtures.append(formatted_fixture)

        return gameweek_fixtures

    def retrieve_gameweek_deadline(self, gameweek_no: int) -> datetime:
        request_response = requests.get(url=f"{self.base_url}/bootstrap-static/")
        raw_gameweek_data = json.loads(request_response.content)["events"]

        gameweek_deadline = raw_gameweek_data[gameweek_no - 1]["deadline_time"]

        # Convert to datetime obj
        gameweek_deadline_obj_unaware = datetime.strptime(
            gameweek_deadline, "%Y-%m-%dT%H:%M:%SZ"
        )

        gameweek_deadline_aware = self.timezone.localize(gameweek_deadline_obj_unaware)

        return gameweek_deadline_aware

    def retrieve_gameday_dates(self, gameweek_no: int) -> Set[datetime]:
        request_response = requests.get(
            url=f"{self.base_url}/fixtures?event={gameweek_no}"
        )

        raw_gameweek_data = json.loads(request_response.content)

        gameday_dates = {
            datetime.strptime(fixture["kickoff_time"], "%Y-%m-%dT%H:%M:%SZ")
            for fixture in raw_gameweek_data
        }

        gameday_dates_aware = set()
        for gameday_datetime in gameday_dates:
            # Reset H:M:S to midnight, add tzinfo to each datetime,
            gameday_date = gameday_datetime.date()
            gameday_datetime_midnight = datetime.combine(
                gameday_date, datetime.min.time()
            )

            gameday_datetime_aware = self.timezone.localize(gameday_datetime_midnight)

            gameday_dates_aware.add(gameday_datetime_aware)

        return gameday_dates_aware


if __name__ == "__main__":
    fpl_interface = FPLInterface()
    results = fpl_interface.retrieve_weekly_scorers(gameweek_no=1)
