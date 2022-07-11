from datetime import date, datetime
from unittest import TestCase
from unittest.mock import Mock, patch

from freezegun import freeze_time

from fantasy_funball.logic.choices import (
    determine_player_played_in_fixture,
    determine_players_fixture_has_finished,
    has_gameweek_ended,
    is_deadline_day,
)
from fantasy_funball.models import Fixture, Gameday, Gameweek, Player

CHOICES_LOGIC_PATH = "fantasy_funball.logic.choices"


class TestChoices(TestCase):
    def setUp(self) -> None:
        pass

    @patch(f"{CHOICES_LOGIC_PATH}.date")
    @patch(f"{CHOICES_LOGIC_PATH}.Gameweek.objects.get")
    def _is_deadline_day_test(
        self,
        mock_get_gameweek,
        mock_date,
        test_date,
    ) -> bool:
        mock_gameweek = Mock(spec=Gameweek)
        mock_gameweek.deadline = datetime(
            year=2022, month=1, day=1, hour=12, minute=0, second=0
        )
        mock_get_gameweek.return_value = mock_gameweek

        mock_date.today.return_value = test_date

        output = is_deadline_day(
            gameweek_no=1,  # arbitrary input
        )

        return output

    def test_is_deadline_day__true(self):
        output = self._is_deadline_day_test(test_date=date(year=2022, month=1, day=2))

        self.assertTrue(output)

    def test_is_deadline_day__false(self):
        output = self._is_deadline_day_test(test_date=date(year=2022, month=1, day=3))

        self.assertFalse(output)

    @patch(f"{CHOICES_LOGIC_PATH}.date")
    @patch(f"{CHOICES_LOGIC_PATH}.Gameday.objects.filter")
    def _has_gameweek_ended_test(self, mock_get_gamedays, mock_date, test_date) -> bool:
        mock_gameday_one = Mock(spec=Gameday)
        mock_gameday_one.date = datetime(
            year=2022,
            month=1,
            day=3,
            hour=12,
            minute=0,
            second=0,
        )

        mock_gameday_two = Mock(spec=Gameday)
        mock_gameday_two.date = datetime(
            year=2022,
            month=1,
            day=2,
            hour=12,
            minute=0,
            second=0,
        )

        mock_gameday_three = Mock(spec=Gameday)
        mock_gameday_three.date = datetime(
            year=2022,
            month=1,
            day=1,
            hour=12,
            minute=0,
            second=0,
        )

        mock_get_gamedays.return_value = [
            mock_gameday_one,
            mock_gameday_two,
            mock_gameday_three,
        ]

        mock_date.today.return_value = test_date

        output = has_gameweek_ended(gameweek_no=1)  # arbitrary input

        return output

    def test_has_gameweek_ended__true(self):
        output = self._has_gameweek_ended_test(test_date=date(year=2022, month=1, day=4))

        self.assertTrue(output)

    def test_has_gameweek_ended__false(self):
        output = self._has_gameweek_ended_test(test_date=date(year=2022, month=1, day=5))

        self.assertFalse(output)

    def _determine_plays_fixture_has_finished_test(self) -> bool:
        mock_player = Mock(spec=Player)
        mock_player.team = "Spurs"

        mock_fixture = Mock(spec=Fixture)
        mock_fixture.home_team = "Spurs"
        mock_fixture.away_team = "Aston Villa"
        mock_fixture.kickoff = "2022-01-01 12:00:00"

        mock_fixtures = [mock_fixture]

        output = determine_players_fixture_has_finished(
            weekly_fixtures=mock_fixtures,
            player=mock_player,
        )
        return output

    @freeze_time("2022-01-02")
    def test_determine_players_fixture_has_finished__true(self):
        output = self._determine_plays_fixture_has_finished_test()
        self.assertTrue(output)

    @freeze_time("2022-01-01")
    def test_determine_players_fixture_has_finished__false(self):
        output = self._determine_plays_fixture_has_finished_test()
        self.assertFalse(output)

    def _determine_player_played_in_fixture_test(self, minutes_played):
        mock_player = Mock(spec=Player)
        mock_player.surname = "Kulusevski"
        mock_player.team.team_name = "Spurs"

        mock_fpl_players = [
            {
                "id": 21,
                "surname": "Kulusevski",
                "team": "Spurs",
            }
        ]

        mock_raw_gameweek_player_data = [
            {
                "id": 21,
                "stats": {
                    "minutes": minutes_played,
                },
            }
        ]

        output = determine_player_played_in_fixture(
            player=mock_player,
            fpl_players=mock_fpl_players,
            raw_gameweek_player_data=mock_raw_gameweek_player_data,
        )

        return output

    def test_determine_player_played_in_fixture__true(self):
        output = self._determine_player_played_in_fixture_test(
            minutes_played=1,
        )

        self.assertTrue(output)

    def test_determine_player_played_in_fixture__false(self):
        output = self._determine_player_played_in_fixture_test(
            minutes_played=0,
        )

        self.assertFalse(output)
