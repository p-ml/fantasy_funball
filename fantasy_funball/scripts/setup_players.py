from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Player, Team
from fantasy_funball.scripts.db_connection import database_connection


def setup_players() -> None:
    # Wipe postgres player table before adding setting up
    conn = database_connection()
    cur = conn.cursor()
    cur.execute(
        "truncate fantasy_funball_player, "
        "fantasy_funball_result_assists,"
        "fantasy_funball_result_scorers,"
        "fantasy_funball_choices;"
    )
    conn.commit()
    conn.close()

    fpl_interface = FPLInterface()
    players = fpl_interface.retrieve_players()

    for player in players:
        team_obj = Team.objects.get(team_name=player["team"])

        player_obj = Player(
            first_name=player["first_name"],
            surname=player["surname"],
            team=team_obj,
            position=player["position"],
        )

        player_obj.save()


if __name__ == "__main__":
    setup_players()
