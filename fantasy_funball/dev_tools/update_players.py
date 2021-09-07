import logging

from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Player

logger = logging.getLogger("papertrail")


def update_players():
    """Removes players in db that are not present in FPL API"""
    fpl_interface = FPLInterface()
    fpl_players = fpl_interface.retrieve_players()

    db_players = list(Player.objects.all())
    for db_player in db_players:
        try:
            _ = next(
                player
                for player in fpl_players
                if player["first_name"] == db_player.first_name
                and player["surname"] == db_player.surname
                and player["team"] == db_player.team.team_name
            )
        except StopIteration:
            # If player doesn't exist in FPL API, then delete from db
            logger.info(
                f"{db_player.first_name} {db_player.surname} playing for "
                f"{db_player.team.team_name} has been removed"
            )
            db_player.delete()


if __name__ == "__main__":
    update_players()
