from datetime import datetime

import pytz


def get_current_datetime() -> datetime:
    """Get local datetime, factors BST"""
    current_datetime_tz_unaware = datetime.now()
    bst = pytz.timezone("Europe/London")
    current_datetime = bst.localize(current_datetime_tz_unaware)

    return current_datetime


def determine_if_transfer_window() -> bool:
    """Determines if we are in a transfer window"""
    bst = pytz.timezone("Europe/London")

    winter_tf_window_start = datetime(
        day=1,
        month=1,
        year=2022,
        tzinfo=bst,
    )

    winter_tf_window_end = datetime(
        day=1,
        month=2,
        year=2022,
        tzinfo=bst,
    )

    current_time = get_current_datetime()

    if winter_tf_window_start < current_time < winter_tf_window_end:
        return True

    else:
        return False


if __name__ == "__main__":
    is_tf_window = determine_if_transfer_window()
