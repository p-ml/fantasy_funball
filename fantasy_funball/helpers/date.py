from datetime import datetime

import pytz


def get_current_datetime() -> datetime:
    """Get local datetime, factors BST"""
    current_datetime_tz_unaware = datetime.now()
    bst = pytz.timezone("Europe/London")
    current_datetime = bst.localize(current_datetime_tz_unaware)

    return current_datetime


if __name__ == "__main__":
    current_datetime = get_current_datetime()
