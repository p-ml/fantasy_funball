from datetime import datetime

import django
import pytz

django.setup()

from fantasy_funball.models import Gameweek


def determine_gameweek_no():
    """Uses local time to determine what gameweek number we are in"""
    # Retrieve list of gameweek objects, sorted by deadline
    gameweek_info = list(Gameweek.objects.order_by("deadline"))

    # Get current datetime
    current_datetime_tz_unaware = datetime.now()
    utc = pytz.timezone("UTC")
    current_datetime = utc.localize(current_datetime_tz_unaware)

    gameweek_no = 0  # Season hasn't started yet
    for gameweek in gameweek_info:
        if current_datetime > gameweek.deadline:
            gameweek_no = gameweek.gameweek_no

    return gameweek_no


if __name__ == "__main__":
    determine_gameweek_no()
