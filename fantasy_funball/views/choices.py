import logging

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

logger = logging.getLogger("papertrail")


class FunballerGetChoiceView(APIView):
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
                "player_point_awarded",
                "team_point_awarded",
                "player_has_been_steved",
                "team_has_been_steved",
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


class FunballerPostChoiceView(APIView):
    def post(self, request: WSGIRequest, pin: str) -> Response:
        """Adds a funballer's choice to postgres db"""
        gameweek_no = request.data["gameweek_no"]
        gameweek_obj = Gameweek.objects.get(gameweek_no=gameweek_no)

        # Get funballer by pin
        funballer = Funballer.objects.get(pin=pin)
        funballer_name = funballer.first_name

        team_choice = request.data["team_choice"]
        player_choice = int(request.data["player_choice"])

        deadline_passed_check = request.data.get("deadline_passed_check", True)

        if deadline_passed_check:
            check_for_passed_deadline(gameweek_deadline=gameweek_obj.deadline)

        # Check if team/player has already been selected
        team_selection_check(
            funballer_first_name=funballer_name,
            team_name=team_choice,
        )

        player_selection_check(
            funballer_first_name=funballer_name,
            player_id=player_choice,
        )

        # Check if selection for this gameweek has already been submitted
        try:
            existing_choice = Choices.objects.get(
                funballer_id=Funballer.objects.get(first_name=funballer_name),
                gameweek_id=gameweek_obj,
            )

            try:
                updated_team = Team.objects.get(team_name=team_choice)
            except Team.DoesNotExist:
                raise TeamNotFoundError(f"Team with name {team_choice} not found")

            try:
                updated_player = Player.objects.get(id=player_choice)
            except Player.DoesNotExist:
                raise PlayerNotFoundError(f"Player with id {player_choice} not found")

            existing_choice.team_choice = updated_team
            existing_choice.player_choice = updated_player
            existing_choice.save()

            logger.info(
                f"Funballer {funballer_name} has successfully updated their choice for "
                f"gameweek {gameweek_no}: {updated_team} and {updated_player}"
            )

            return Response(status=status.HTTP_200_OK, data="Choice updated")

        except Choices.DoesNotExist:
            # Create new choice if it doesn't already exist
            funballer_id = Funballer.objects.get(first_name=funballer_name).id
            team = Team.objects.get(team_name=request.data["team_choice"])

            player = Player.objects.get(id=player_choice)

            choice = Choices(
                funballer_id=funballer_id,
                gameweek_id=gameweek_obj.id,
                team_choice=team,
                player_choice=player,
            )
            choice.save()

            logger.info(
                f"Funballer {funballer_name} has successfully submitted their choice for "
                f"gameweek {gameweek_no}: {team.team_name} and {player.first_name} "
                f"{player.surname}"
            )

            return Response(status=status.HTTP_201_CREATED, data="Choice submitted")


class FunballerRemainingTeamChoice(APIView):
    def get(self, request: WSGIRequest, funballer_name: str) -> Response:
        """
        Returns the name of each team and how many times the requested funballer
        can choose them.
        """
        team_selection_limit = 2

        try:
            choices = Choices.objects.filter(
                funballer_id__first_name=funballer_name,
            ).values("team_choice__team_name")
        except Choices.DoesNotExist:
            raise ChoicesNotFoundError(f"Choices for {funballer_name} not found")

        all_teams = Team.objects.all().values("team_name")

        all_team_names = [
            team["team_name"]
            for team in all_teams
            if team["team_name"] != "Gameweek Void"
        ]

        team_choices = [choice["team_choice__team_name"] for choice in choices]

        valid_team_selections = [
            {
                "team_name": team,
                "remaining_selections": team_selection_limit - team_choices.count(team),
            }
            for team in all_team_names
        ]

        return Response(status=status.HTTP_201_CREATED, data=valid_team_selections)
