from datetime import datetime

import pytz

from fantasy_funball.logic import determine_gameweek_no


def get_current_datetime() -> datetime:
    """Get local datetime, factors BST"""
    current_datetime_tz_unaware = datetime.now()
    bst = pytz.timezone("Europe/London")
    current_datetime = bst.localize(current_datetime_tz_unaware)

    return current_datetime


if __name__ == "__main__":
    current_gameweek_no = determine_gameweek_no()
