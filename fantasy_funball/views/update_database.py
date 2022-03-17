from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fantasy_funball.logic.helpers import determine_gameweek_no
from fantasy_funball.logic.results import update_results
from fantasy_funball.logic.standings import update_standings


class UpdateDatabaseView(APIView):
    def get(self, request: WSGIRequest) -> Response:
        """Endpoint to check for results and update standings"""
        gameweek_no = determine_gameweek_no()
        update_results(gameweek_no=gameweek_no)
        update_standings(gameweek_no=gameweek_no)

        return Response(status=status.HTTP_200_OK)
