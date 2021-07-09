from django.core.handlers.wsgi import WSGIRequest
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import (
    FixtureNotFoundError,
    GamedayNotFoundError,
    GameweekNotFoundError,
)
from fantasy_funball.models import Fixture, Gameday, Gameweek


class RetrieveFixture(APIView):
    """Viewset to handle fixtures"""

    def get(self, request: WSGIRequest, id: int) -> Response:
        """Retrieve fixture from postgres"""
        # TODO: Might want to do this by team name and date

        try:
            fixture = Fixture.objects.get(id=id)
        except Fixture.DoesNotExist:
            raise FixtureNotFoundError(f"Fixture with id {id} not found")

        # Convert to json for output
        formatted_fixture = model_to_dict(fixture)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_fixture,
        )


class RetrieveGameday(APIView):
    """Viewset to handle gamedays"""

    def get(self, request: WSGIRequest, id: int) -> Response:
        """Retrieve gameday from postgres"""
        # TODO: Might want to do this by date

        try:
            gameday = Gameday.objects.get(id=id)
        except Gameday.DoesNotExist:
            raise GamedayNotFoundError(f"Gameday with id {id} not found")

        # Convert to json for output
        formatted_gameday = model_to_dict(gameday)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_gameday,
        )


class RetrieveGameweek(APIView):
    """Viewset to handle gameweeks"""

    def get(self, request: WSGIRequest, gameweek_no: int) -> Response:
        """Retrieve all matches from a gameweek from postgres by
        gameweek number (1-38)"""

        try:
            # Get gameweek id using gameweek no
            gameweek = Gameweek.objects.get(gameweek_no=gameweek_no)
            gameweek_fixtures = Fixture.objects.filter(
                gameday__gameweek_id=gameweek.id,
            ).values(
                "id",
                "home_team",
                "away_team",
                "kickoff",
                "gameday__date",
            )
        except Gameweek.DoesNotExist:
            raise GameweekNotFoundError(f"Gameweek number {gameweek_no} not found")

        # Convert to json for output
        formatted_gameweek = list(gameweek_fixtures)

        # Parse game date from datetime obj to str
        for game in formatted_gameweek:
            game["gameday__date"] = game["gameday__date"].strftime("%a %-d %b %-y")

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_gameweek,
        )
