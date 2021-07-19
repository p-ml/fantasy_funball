from datetime import datetime
from typing import Union

import pytz
from django.core.handlers.wsgi import WSGIRequest
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import (
    ChoicesNotFoundError,
    FunballerNotFoundError,
    GameweekDeadlinePassedError,
)
from fantasy_funball.models import Choices, Funballer, Gameweek
from fantasy_funball.models.players import Player
from fantasy_funball.models.teams import Team


class FunballerViewMixin:
    @staticmethod
    def _get_funballer_by_id(id: int) -> Union[Funballer, None]:
        try:
            return Funballer.objects.get(id=id)
        except Funballer.DoesNotExist:
            raise FunballerNotFoundError(f"Funballer with id {id} not found")


class FunballerView(APIView, FunballerViewMixin):
    """Viewset to handle funballers"""

    def post(self, request: WSGIRequest) -> Response:
        """Add a funballer to postgres db"""
        funballer = Funballer(**request.data)
        funballer.save()

        # Convert to json for output
        formatted_funballer = model_to_dict(funballer)

        return Response(
            status=status.HTTP_201_CREATED,
            data=formatted_funballer,
        )

    def get(self, request: WSGIRequest) -> Response:
        """Retrieve all funballers from postgres db"""
        funballers = Funballer.objects.all()

        formatted_funballers = [model_to_dict(funballer) for funballer in funballers]

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_funballers,
        )


class SingleFunballerView(APIView, FunballerViewMixin):
    def get(self, request: WSGIRequest, id: int) -> Response:
        """Retrieve a funballer from postgres db"""
        funballer = self._get_funballer_by_id(id=id)

        # Convert to json for output
        formatted_funballer = model_to_dict(funballer)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_funballer,
        )

    def patch(self, request: WSGIRequest, id: int) -> Response:
        """Update a funballer in postgres db"""
        funballer = self._get_funballer_by_id(id=id)

        # Parse update payload
        update_payload = [
            {"field": str(key), "value": str(value)}
            for key, value in request.data.items()
        ]

        # Update funballer attribute
        setattr(funballer, update_payload[0]["field"], update_payload[0]["value"])
        funballer.save()

        # Convert to json for output
        formatted_funballer = model_to_dict(funballer)

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_funballer,
        )

    def delete(self, request: WSGIRequest, id: int) -> Response:
        """Delete a funballer from postgres db"""
        funballer = self._get_funballer_by_id(id=id)
        funballer.delete()

        return Response(status=status.HTTP_200_OK)


class FunballerChoiceView(APIView):
    def get(self, request: WSGIRequest, funballer_name: str) -> Response:
        """Retrieve all of a funballers choices from postgres db"""

        try:
            choices = Choices.objects.filter(
                funballer_id__first_name=funballer_name,
            ).values(
                "funballer_id__first_name",
                "gameweek_id__gameweek_no",
                "team_choice__team_name",
                "player_choice__first_name",
                "player_choice__surname",
            )
        except Choices.DoesNotExist:
            raise ChoicesNotFoundError(f"Choices for {funballer_name} not found")
        formatted_choices = sorted(
            list(choices), key=lambda x: x["gameweek_id__gameweek_no"]
        )

        return Response(
            status=status.HTTP_200_OK,
            data=formatted_choices,
        )

    def post(self, request: WSGIRequest, funballer_name: str) -> Response:
        """Adds a funballer's choice to postgres db"""
        # Check if gameweek deadline has passed
        gameweek_no = request.data["gameweek_no"]
        gameweek_obj = Gameweek.objects.get(gameweek_no=gameweek_no)
        gameweek_deadline = gameweek_obj.deadline

        # Current utc time
        current_time = datetime.now()
        utc = pytz.UTC
        current_time = utc.localize(current_time)

        if current_time > gameweek_deadline:
            raise GameweekDeadlinePassedError

        # Check if selection for this gameweek has already been submitted
        try:
            existing_choice = Choices.objects.get(
                funballer_id=Funballer.objects.get(first_name=funballer_name),
                gameweek_id=Gameweek.objects.get(
                    gameweek_no=gameweek_no,
                ),
            )

            updated_team = Team.objects.get(team_name=request.data["team_choice"])
            updated_player = Player.objects.get(
                first_name=request.data["player_choice"].split(" ")[0],
                surname=request.data["player_choice"].split(" ")[1],
            )

            existing_choice.team_choice = updated_team
            existing_choice.player_choice = updated_player
            existing_choice.save()

            return Response(status=status.HTTP_200_OK, data="Choice updated")

        except Choices.DoesNotExist:
            # Create new choice if it doesn't already exist
            choice = Choices(
                funballer_id=Funballer.objects.get(first_name=funballer_name),
                gameweek_id=Gameweek.objects.get(
                    gameweek_no=gameweek_no,
                ),
                team_choice=Team.objects.get(team_name=request.data["team_choice"]),
                player_choice=Player.objects.get(
                    first_name=request.data["player_choice"].split(" ")[0],
                    surname=request.data["player_choice"].split(" ")[1],
                ),
            )
            choice.save()

            return Response(status=status.HTTP_201_CREATED, data="Choice submitted")
