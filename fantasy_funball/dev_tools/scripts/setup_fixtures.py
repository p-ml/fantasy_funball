import logging

from fantasy_funball.dev_tools.scripts.db_connection import database_connection
from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Fixture

N_GAMEWEEKS = 38
logger = logging.getLogger("papertrail")


def setup_fixtures():
    # Wipe postgres db fixture table before adding setting up
    conn = database_connection()
    cur = conn.cursor()
    cur.execute(
        "truncate fantasy_funball_fixture,"
        "fantasy_funball_result,"
        "fantasy_funball_assists,"
        "fantasy_funball_goals,"
        "fantasy_funball_choices;"
    )
    conn.commit()
    conn.close()

    fpl_interface = FPLInterface()

    for gameweek_no in range(1, N_GAMEWEEKS + 1):
        logger.info(f"Setting up fixtures for gameweek {gameweek_no}")
        gameweek_fixtures = fpl_interface.retrieve_gameweek_fixtures(
            gameweek_no=gameweek_no,
        )

        for fixture in gameweek_fixtures:
            fixture_obj = Fixture(
                home_team=fixture["home_team"],
                away_team=fixture["away_team"],
                gameday=fixture["gameday"],
                kickoff=fixture["kickoff"],
            )

            fixture_obj.save()


if __name__ == "__main__":
    setup_fixtures()
