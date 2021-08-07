from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Team
from fantasy_funball.scripts.db_connection import database_connection


def setup_teams() -> None:
    # Wipe postgres team table before adding setting up
    conn = database_connection()
    cur = conn.cursor()
    cur.execute(
        "truncate fantasy_funball_player, "
        "fantasy_funball_result_assists,"
        "fantasy_funball_result_scorers,"
        "fantasy_funball_team,"
        "fantasy_funball_result,"
        "fantasy_funball_fixture,"
        "fantasy_funball_choices;"
    )
    conn.commit()
    conn.close()

    fpl_interface = FPLInterface()
    teams = fpl_interface.retrieve_teams()

    for team_name in teams.values():
        team_inst = Team(team_name=team_name)
        team_inst.save()
