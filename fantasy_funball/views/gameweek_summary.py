from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fantasy_funball.models import GameweekSummary


class GameweekSummaryViewset(APIView):
    """Viewset for updating & retrieving gameweek summary"""

    def get(self, request: WSGIRequest) -> Response:
        """Retrieve gameweek summary"""

        # Get gameweek summary
        gameweek_summary = GameweekSummary.objects.all().values(
            "text",
        )

        # Convert to json for output
        formatted_gameweeks = list(gameweek_summary)[0]

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_gameweeks,
        )

    def put(self, request: WSGIRequest) -> Response:
        """Update gameweek summary"""
        # Only need 1 record, that overwrites itself on each PUT

        # Check if gameweek summary exists
        gameweek_summary = list(GameweekSummary.objects.all())
        if gameweek_summary == []:
            gameweek_summary = GameweekSummary(
                text=request.data["text"],
            )
            gameweek_summary.save()

        else:
            gameweek_summary[0].text = request.data["text"]
            gameweek_summary[0].save()

        return Response(
            status=status.HTTP_201_CREATED,
        )
