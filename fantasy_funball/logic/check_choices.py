"""At midnight of deadline day, checks if all players have made a choice
If they haven't, Steve them"""
from datetime import date, timedelta
from typing import List

import django

from fantasy_funball.logic.random_generator import get_random_player, get_random_team

django.setup()

import logging

from fantasy_funball.models import Choices, Funballer, Gameweek

log = logging.getLogger(__name__)


def is_deadline_day(gameweek_no: int) -> bool:
    """Checks if today is gameweek deadline day"""
    log.info("Checking if today is deadline day...")

    gameweek = Gameweek.objects.get(gameweek_no=gameweek_no)
    gameweek_deadline_date = gameweek.deadline.date()

    # When this func returns true, todays_date will be midnight (UTC) next day
    # So go back one day
    todays_date = date.today()
    todays_date = todays_date - timedelta(days=1)

    if todays_date == gameweek_deadline_date:
        log.info("Today is deadline day")
        return True

    else:
        log.info("Today is not deadline day")
        return False


def check_choices(gameweek_no: int):
    """If we're in deadline day, check all funballers have submitted a choice"""
    deadline_day = is_deadline_day(gameweek_no=gameweek_no)

    if deadline_day:
        log.info("Checking for funballers who haven't submitted choices...")

        choices = list(
            Choices.objects.filter(
                gameweek__gameweek_no=gameweek_no,
            )
        )

        funballer_with_choice_ids = [choice.funballer_id for choice in choices]

        all_funballers = list(Funballer.objects.all())

        funballers_with_no_choices = [
            funballer
            for funballer in all_funballers
            if funballer.id not in funballer_with_choice_ids
        ]

        allocate_choices(
            funballers_with_no_choices=funballers_with_no_choices,
            gameweek_no=gameweek_no,
        )


def allocate_choices(
    funballers_with_no_choices: List[Funballer],
    gameweek_no: int,
):
    """Allocate a random team/player to each funballer who has not picked"""
    for funballer in funballers_with_no_choices:
        log.info("Allocating random choices...")

        # Get list of teams already chosen by funballer
        all_funballer_choices = list(Choices.objects.filter(funballer=funballer))

        # Get all funballer's team picks
        funballer_team_choices = [
            choice.team_choice for choice in all_funballer_choices
        ]

        # Get all funballer's player picks
        funballer_player_choices = [
            choice.player_choice for choice in all_funballer_choices
        ]

        random_team = get_random_team(non_permitted_teams=funballer_team_choices)
        random_player = get_random_player(
            non_permitted_players=funballer_player_choices
        )

        # Get gameweek obj from gameweek no
        gameweek = Gameweek.objects.get(gameweek_no=gameweek_no)

        choice = Choices(
            funballer_id=funballer.id,
            gameweek=gameweek,
            team_choice=random_team,
            player_choice=random_player,
        )

        choice.save()


if __name__ == "__main__":
    all_funballers = list(Funballer.objects.all())
    allocate_choices(funballers_with_no_choices=all_funballers, gameweek_no=1)
