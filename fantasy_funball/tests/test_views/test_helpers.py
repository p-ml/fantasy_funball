from datetime import datetime
from unittest import TestCase

import pytz

from core.exceptions import GameweekDeadlinePassedError
from fantasy_funball.views.helpers import check_for_passed_deadline


class TestHelpers(TestCase):
    def test_check_for_passed_deadline(self):
        past_deadline = datetime(year=2000, month=1, day=1)

        utc = pytz.UTC
        past_deadline_aware = utc.localize(past_deadline)

        with self.assertRaises(GameweekDeadlinePassedError) as ex:
            check_for_passed_deadline(gameweek_deadline=past_deadline_aware)

        self.assertEqual(
            str(ex.exception),
            "Choice cannot be updated/submitted once a gameweek " "deadline has passed",
        )
        self.assertEqual(ex.exception.status_code, 400)
