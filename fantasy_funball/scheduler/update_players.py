import logging

from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Player, Team

logger = logging.getLogger("papertrail")


def add_players():
    """Adds new players to the database"""
    fpl_interface = FPLInterface()
    players = fpl_interface.retrieve_players()

    for player in players:
        # Check if player exists, if not, add to db

        # Checking team accounts for transfers between PL teams
        team_obj = Team.objects.get(team_name=player["team"])

        try:
            Player.objects.get(
                first_name=player["first_name"],
                surname=player["surname"],
                team=team_obj,
                position=player["position"],
            )

        except Player.DoesNotExist:
            team_obj = Team.objects.get(team_name=player["team"])

            player_obj = Player(
                first_name=player["first_name"],
                surname=player["surname"],
                team=team_obj,
                position=player["position"],
            )
            player_obj.save()

            print(
                f"{player['first_name']} {player['surname']}, playing for "
                f"{player['team']} has been added."
            )

        else:
            continue


def remove_players():
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


def update_players():
    """
    Keeps players in the db up to date.
    Will only run during transfer window.
    """
    add_players()
    remove_players()


if __name__ == "__main__":
    update_players()
