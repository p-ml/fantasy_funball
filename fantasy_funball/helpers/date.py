from datetime import datetime, timedelta

import django
import pytz

from fantasy_funball.logic.determine_gameweek import determine_gameweek_no

django.setup()

from fantasy_funball.models import Gameday


def get_current_datetime() -> datetime:
    """Get local datetime, factors BST"""
    current_datetime_tz_unaware = datetime.now()
    bst = pytz.timezone("Europe/London")
    current_datetime = bst.localize(current_datetime_tz_unaware)

    return current_datetime


def is_first_day_of_gameweek(current_gameweek_no: int):
    """Checks if today is first day of the gameweek"""
    # Get all gamedays in previous gameweek
    previous_gameweek_no = current_gameweek_no - 1
    gameweek_gamedays = list(
        Gameday.objects.filter(
            gameweek__gameweek_no=previous_gameweek_no,
        )
    )

    # Sort by date
    gameweek_gamedays.sort(key=lambda x: x.date, reverse=True)
    final_gameday_date = gameweek_gamedays[0].date
    first_day_of_gameweek = final_gameday_date + timedelta(days=1)
    first_day_of_gameweek_date = first_day_of_gameweek.date()

    # Get todays date, make BST aware
    bst = pytz.timezone("Europe/London")
    todays_date = bst.localize(datetime.today()).date()

    if first_day_of_gameweek_date == todays_date:
        return True
    else:
        return False


if __name__ == "__main__":
    current_gameweek_no = determine_gameweek_no()
    current_datetime = is_first_day_of_gameweek(current_gameweek_no)
