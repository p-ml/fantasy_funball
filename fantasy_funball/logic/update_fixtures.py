import logging

import django

from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.helpers.date import is_first_day_of_gameweek
from fantasy_funball.logic.determine_gameweek import determine_gameweek_no
from fantasy_funball.models import Fixture, Gameday, Gameweek

django.setup()

logger = logging.getLogger("papertrail")


def wipe_upcoming_gameweek_fixtures() -> None:
    next_gameweek_no = determine_gameweek_no() + 1

    # First wipe all fixtures
    stored_fixtures = list(
        Fixture.objects.filter(gameday__gameweek__gameweek_no=next_gameweek_no)
    )

    for fixture in stored_fixtures:
        fixture.delete()

    # Then delete gamedays
    stored_gamedays = list(
        Gameday.objects.filter(gameweek__gameweek_no=next_gameweek_no)
    )

    for gameday in stored_gamedays:
        gameday.delete()


def insert_new_gamedays() -> None:
    next_gameweek_no = determine_gameweek_no() + 1

    fpl_interface = FPLInterface()
    fpl_interface_gameday_dates = fpl_interface.retrieve_gameday_dates(
        gameweek_no=next_gameweek_no,
    )

    gameweek_obj = Gameweek.objects.get(gameweek_no=next_gameweek_no)

    for new_gameday_date in fpl_interface_gameday_dates:
        gameday_obj = Gameday(
            date=new_gameday_date,
            gameweek=gameweek_obj,
        )
        gameday_obj.save()


def insert_new_fixtures() -> None:
    next_gameweek_no = determine_gameweek_no() + 1

    fpl_interface = FPLInterface()
    gameweek_fixtures = fpl_interface.retrieve_gameweek_fixtures(
        gameweek_no=next_gameweek_no,
    )

    for fixture in gameweek_fixtures:
        fixture_obj = Fixture(
            home_team=fixture["home_team"],
            away_team=fixture["away_team"],
            gameday=fixture["gameday"],
            kickoff=fixture["kickoff"],
        )

        fixture_obj.save()


def update_gameweek_deadlines() -> None:
    next_gameweek_no = determine_gameweek_no() + 1

    fpl_interface = FPLInterface()
    updated_gameweek_deadline = fpl_interface.retrieve_gameweek_deadline(
        gameweek_no=next_gameweek_no,
    )

    gameweek_obj = Gameweek.objects.get(
        gameweek_no=next_gameweek_no,
    )

    if gameweek_obj.deadline != updated_gameweek_deadline:
        gameweek_obj.deadline = updated_gameweek_deadline
        gameweek_obj.save()


def update_fixtures(gameweek_no: int) -> None:
    first_day_of_gameweek = is_first_day_of_gameweek(
        current_gameweek_no=gameweek_no
    )
    if first_day_of_gameweek:
        logger.info(
            f"Refreshing fixtures for upcoming gameweek ({gameweek_no+1})..."
        )
        wipe_upcoming_gameweek_fixtures()
        insert_new_gamedays()
        insert_new_fixtures()
        update_gameweek_deadlines()


if __name__ == "__main__":
    wipe_upcoming_gameweek_fixtures()
    insert_new_gamedays()
    insert_new_fixtures()
    update_gameweek_deadlines()
