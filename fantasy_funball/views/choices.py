from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import ChoicesNotFoundError, PlayerNotFoundError, TeamNotFoundError
from fantasy_funball.models import Choices, Funballer, Gameweek, Player, Team
from fantasy_funball.views.helpers import (
    check_for_passed_deadline,
    player_selection_check,
    team_selection_check,
)


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
        gameweek_no = request.data["gameweek_no"]
        gameweek_obj = Gameweek.objects.get(gameweek_no=gameweek_no)

        check_for_passed_deadline(gameweek_deadline=gameweek_obj.deadline)

        # Check if team/player has already been selected
        team_selection_check(
            funballer_first_name=funballer_name, team_name=request.data["team_choice"]
        )
        player_selection_check(
            funballer_first_name=funballer_name,
            player_name=request.data["player_choice"],
        )

        # Check if selection for this gameweek has already been submitted
        try:
            existing_choice = Choices.objects.get(
                funballer_id=Funballer.objects.get(first_name=funballer_name),
                gameweek_id=gameweek_obj,
            )

            try:
                updated_team = Team.objects.get(team_name=request.data["team_choice"])
            except Team.DoesNotExist:
                raise TeamNotFoundError(
                    f"Team with name {request.data['team_choice']} not found"
                )

            try:
                updated_player = Player.objects.get(
                    first_name=request.data["player_choice"].split(" ")[0],
                    surname=request.data["player_choice"].split(" ")[1],
                )
            except Player.DoesNotExist:
                raise PlayerNotFoundError(
                    f"Player with name {request.data['player_choice']} not found"
                )

            existing_choice.team_choice = updated_team
            existing_choice.player_choice = updated_player
            existing_choice.save()

            return Response(status=status.HTTP_200_OK, data="Choice updated")

        except Choices.DoesNotExist:
            # Create new choice if it doesn't already exist
            choice = Choices(
                funballer_id=Funballer.objects.get(first_name=funballer_name),
                gameweek_id=gameweek_obj,
                team_choice=Team.objects.get(team_name=request.data["team_choice"]),
                player_choice=Player.objects.get(
                    first_name=request.data["player_choice"].split(" ")[0],
                    surname=request.data["player_choice"].split(" ")[1],
                ),
            )
            choice.save()

            return Response(status=status.HTTP_201_CREATED, data="Choice submitted")
