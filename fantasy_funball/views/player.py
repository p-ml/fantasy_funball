from django.core.handlers.wsgi import WSGIRequest
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import TeamNotFoundError
from fantasy_funball.models import Player, Team


class PlayerTeamView(APIView):
    def get(self, request: WSGIRequest, team_name: str) -> Response:
        try:
            team_players = Player.objects.filter(
                team__team_name=team_name,
            )
        except Team.DoesNotExist:
            raise TeamNotFoundError(f"{team_name} not found")

        formatted_team_players = [model_to_dict(player) for player in team_players]

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_team_players,
        )
