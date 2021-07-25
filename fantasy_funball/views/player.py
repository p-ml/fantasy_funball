from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import TeamNotFoundError
from fantasy_funball.models import Player, Result, Team


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
            player["goals"] = Result.objects.filter(scorers=player["id"]).count()
            player["assists"] = Result.objects.filter(assists=player["id"]).count()

        formatted_team_players = list(team_players)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_team_players,
        )
