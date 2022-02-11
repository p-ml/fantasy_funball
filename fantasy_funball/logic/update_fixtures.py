import logging

import django

from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.logic.check_choices import has_gameweek_ended
from fantasy_funball.models import Fixture, Gameday, Gameweek

django.setup()

logger = logging.getLogger("papertrail")


def wipe_future_gameweek_fixtures(gameweek_no: int) -> None:
    # First wipe all fixtures
    stored_fixtures = list(
        Fixture.objects.filter(gameday__gameweek__gameweek_no=gameweek_no)
    )

    for fixture in stored_fixtures:
        fixture.delete()

    # Then delete gamedays
    stored_gamedays = list(Gameday.objects.filter(gameweek__gameweek_no=gameweek_no))

    for gameday in stored_gamedays:
        gameday.delete()


def insert_new_gamedays(gameweek_no: int) -> None:
    fpl_interface = FPLInterface()
    fpl_interface_gameday_dates = fpl_interface.retrieve_gameday_dates(
        gameweek_no=gameweek_no,
    )

    gameweek_obj = Gameweek.objects.get(gameweek_no=gameweek_no)

    for new_gameday_date in fpl_interface_gameday_dates:
        gameday_obj = Gameday(
            date=new_gameday_date,
            gameweek=gameweek_obj,
        )
        gameday_obj.save()


def insert_new_fixtures(gameweek_no: int) -> None:
    fpl_interface = FPLInterface()
    gameweek_fixtures = fpl_interface.retrieve_gameweek_fixtures(
        gameweek_no=gameweek_no,
    )

    for fixture in gameweek_fixtures:
        fixture_obj = Fixture(
            home_team=fixture["home_team"],
            away_team=fixture["away_team"],
            gameday=fixture["gameday"],
            kickoff=fixture["kickoff"],
        )

        fixture_obj.save()


def update_gameweek_deadlines(gameweek_no: int) -> None:
    fpl_interface = FPLInterface()
    updated_gameweek_deadline = fpl_interface.retrieve_gameweek_deadline(
        gameweek_no=gameweek_no,
    )

    gameweek_obj = Gameweek.objects.get(
        gameweek_no=gameweek_no,
    )

    if gameweek_obj.deadline != updated_gameweek_deadline:
        gameweek_obj.deadline = updated_gameweek_deadline
        gameweek_obj.save()


def update_fixtures(gameweek_no: int) -> None:
    """Run by scheduler"""
    gameweek_ended = has_gameweek_ended(gameweek_no=gameweek_no)
    if gameweek_ended:
        upcoming_gameweek_no = gameweek_no + 1
        logger.info(
            f"Refreshing fixtures for upcoming gameweek ({upcoming_gameweek_no})..."
        )
        wipe_future_gameweek_fixtures(gameweek_no=upcoming_gameweek_no)
        insert_new_gamedays(gameweek_no=upcoming_gameweek_no)
        insert_new_fixtures(gameweek_no=upcoming_gameweek_no)
        update_gameweek_deadlines(gameweek_no=upcoming_gameweek_no)
