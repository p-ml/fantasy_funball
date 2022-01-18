import django

django.setup()

from fantasy_funball.models import Funballer, Gameweek, Gameday, Fixture, Team


class FunctionalTestHarness:
    @staticmethod
    def delete_funballer() -> None:
        funballers = Funballer.objects.filter(
            first_name="functional",
            surname="test",
        )
        for funballer in funballers:
            funballer.delete()

    def _setup_dummy_gameweek(self) -> Gameweek:
        gameweek = Gameweek(
            deadline="2022-01-01 00:00:00",
            gameweek_no=1,
        )
        gameweek.save()

        return gameweek

    def _setup_dummy_gameday(self) -> Gameday:
        gameweek = self._setup_dummy_gameweek()

        gameday = Gameday(
            gameweek=gameweek,
            date="2022-01-01",
        )
        gameday.save()
        return gameday

    def _setup_dummy_teams(self) -> (Team, Team):
        home_team = Team(
            team_name="Tottenham Hotspur",
        )
        home_team.save()

        away_team = Team(
            team_name="Brentford"
        )
        away_team.save()

        return home_team, away_team

    def setup_dummy_fixture(self) -> Fixture:
        gameday = self._setup_dummy_gameday()
        home_team, away_team = self._setup_dummy_teams()

        fixture = Fixture(
            gameday=gameday,
            home_team=home_team,
            away_team=away_team,
            kickoff="2022-01-01 12:00:00",
        )
        fixture.save()

        return fixture

    @staticmethod
    def teardown_dummy_fixture():
        fixtures = Fixture.objects.all()
        for fixture in fixtures:
            fixture.delete()

        gamedays = Gameday.objects.all()
        for gameday in gamedays:
            gameday.delete()

        gameweeks = Gameweek.objects.all()
        for gameweek in gameweeks:
            gameweek.delete()
