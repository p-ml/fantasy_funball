from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import TeamNotFoundError
from fantasy_funball.models import Assists, Goals, Player, Team


class PlayerTeamView(APIView):
    def get(self, request: WSGIRequest, team_name: str) -> Response:
        try:
            team_players = Player.objects.filter(team__team_name=team_name,).values(
                "id",
                "first_name",
                "surname",
            )
        except Team.DoesNotExist:
            raise TeamNotFoundError(f"{team_name} not found")

        for player in team_players:
            player["goals"] = (
                Goals.objects.filter(player_id=player["id"]).aggregate(
                    Sum("goals_scored")
                )["goals_scored__sum"]
                or 0
            )

            player["assists"] = (
                Assists.objects.filter(player_id=player["id"]).aggregate(
                    Sum("assists_made")
                )["assists_made__sum"]
                or 0
            )

        formatted_team_players = list(team_players)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_team_players,
        )


class RetrievePlayerView(APIView):
    def get(self, request: WSGIRequest) -> Response:
        """Retrieve names of all players in db"""
        all_players = Player.objects.all()

        formatted_players = [
            {
                "name": f"{player.first_name} {player.surname}",
                "id": player.id,
            }
            for player in all_players
            if player.surname != "Void"  # Does not return "gameweek void" player
        ]

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_players,
        )


class AddPlayerView(APIView):
    def post(self, request: WSGIRequest) -> Response:
        """Add player to the db"""
        new_player_team = Team.objects.get(team_name=request.data["team_name"])
        new_player = Player(
            first_name=request.data["first_name"],
            surname=request.data["surname"],
            team=new_player_team,
            position=request.data["position"],
        )

        new_player.save()

        confirmation_message = (
            f"Player {request.data['surname']}, playing for {new_player_team.team_name}"
            f" has successfully been added to the database."
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=confirmation_message,
        )
