from fantasy_funball.dev_tools.scripts.db_connection import database_connection
from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Gameweek

N_GAMEWEEKS = 38


def setup_gameweeks():
    # Wipe postgres db gameweek table before adding setting up
    conn = database_connection()
    cur = conn.cursor()
    cur.execute(
        "truncate fantasy_funball_gameweek,"
        "fantasy_funball_gameday,"
        "fantasy_funball_choices,"
        "fantasy_funball_result,"
        "fantasy_funball_fixture,"
        "fantasy_funball_assists,"
        "fantasy_funball_goals;"
    )
    conn.commit()
    conn.close()

    fpl_interface = FPLInterface()

    for gameweek_no in range(1, N_GAMEWEEKS + 1):
        gameweek_deadline = fpl_interface.retrieve_gameweek_deadline(
            gameweek_no=gameweek_no,
        )

        gameweek_obj = Gameweek(
            deadline=gameweek_deadline,
            gameweek_no=gameweek_no,
        )

        gameweek_obj.save()


if __name__ == "__main__":
    setup_gameweeks()
