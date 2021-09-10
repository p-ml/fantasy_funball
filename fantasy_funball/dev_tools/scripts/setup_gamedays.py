from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Gameday, Gameweek
from fantasy_funball.dev_tools.scripts.db_connection import database_connection

N_GAMEWEEKS = 38


def setup_gamedays():
    # Wipe postgres db gameweek/gameday table before adding setting up
    conn = database_connection()
    cur = conn.cursor()
    cur.execute(
        "truncate "
        "fantasy_funball_gameday,"
        "fantasy_funball_choices,"
        "fantasy_funball_result,"
        "fantasy_funball_fixture,"
        "fantasy_funball_result_assists,"
        "fantasy_funball_result_scorers;"
    )
    conn.commit()
    conn.close()

    fpl_interface = FPLInterface()

    for gameweek_no in range(1, N_GAMEWEEKS + 1):
        gameweek_dates = fpl_interface.retrieve_gameday_dates(
            gameweek_no=gameweek_no,
        )

        gameweek_obj = Gameweek.objects.get(gameweek_no=gameweek_no)

        for gameday_date in gameweek_dates:
            gameday_obj = Gameday(
                date=gameday_date,
                gameweek=gameweek_obj,
            )
            gameday_obj.save()


if __name__ == "__main__":
    setup_gamedays()
