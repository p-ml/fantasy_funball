from datetime import datetime

import pytz

from core.exceptions import GameweekDeadlinePassedError


def check_for_passed_deadline(gameweek_deadline: datetime):
    """Raise an error if chosen gameweek has already happened"""
    # Get current utc time
    current_time = datetime.now()
    utc = pytz.UTC
    current_time = utc.localize(current_time)

    if current_time > gameweek_deadline:
        raise GameweekDeadlinePassedError(
            "Choice cannot be updated/submitted for a gameweek"
            "that has already passed"
        )
