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
from fantasy_funball.logic.fixtures import (
    insert_new_fixtures,
    insert_new_gamedays,
    update_gameweek_deadlines,
    wipe_future_gameweek_fixtures,
)
from fantasy_funball.models import Fixture, Gameday, Gameweek


class FixtureViewSet(APIView):
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

    def delete(self, request: WSGIRequest, id: int) -> Response:
        """Delete fixture from postgres db"""
        try:
            fixture = Fixture.objects.get(id=id)
        except Fixture.DoesNotExist:
            raise FixtureNotFoundError(f"Fixture with id {id} not found")

        fixture.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=f"Fixture with id {id} - {fixture.home_team.team_name} vs "
            f"{fixture.away_team.team_name} has been successfully deleted.",
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
                "home_team__team_name",
                "away_team__team_name",
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


class RetrieveAllGameweeks(APIView):
    """Viewset for retrieving all gameweeks"""

    def get(self, request: WSGIRequest) -> Response:
        """Retrieve data stored about all gameweeks (1-38)"""

        # Get all gameweeks
        gameweeks = Gameweek.objects.all().values(
            "gameweek_no",
            "deadline",
        )

        # Convert to json for output
        formatted_gameweeks = list(gameweeks)
        sorted_gameweeks = sorted(formatted_gameweeks, key=lambda x: x["gameweek_no"])

        return Response(
            status=status.HTTP_200_OK,
            data=sorted_gameweeks,
        )


class UpdateGameweekFixtures(APIView):
    def get(self, request: WSGIRequest, gameweek_no: int) -> Response:
        """Refresh/update fixtures for a gameweek"""

        wipe_future_gameweek_fixtures(gameweek_no=gameweek_no)
        insert_new_gamedays(gameweek_no=gameweek_no)
        insert_new_fixtures(gameweek_no=gameweek_no)
        update_gameweek_deadlines(gameweek_no=gameweek_no)

        return Response(
            status=status.HTTP_200_OK,
            data=f"Fixtures for gameweek {gameweek_no} updated successfully",
        )


class InsertGameweekFixtures(APIView):
    def get(self, request: WSGIRequest, gameweek_no: int) -> Response:
        """
        Add fixtures to gameweek, with assumption that gamedays have already been
        set up"""
        insert_new_fixtures(gameweek_no=gameweek_no)

        return Response(
            status=status.HTTP_200_OK,
            data=f"Fixtures for gameweek {gameweek_no} added successfully",
        )
