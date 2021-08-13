from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.models import Player, Team


def update_players():
    """
    Keeps players in the db up to date.
    Will only run during transfer window.
    """
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


if __name__ == "__main__":
    update_players()
