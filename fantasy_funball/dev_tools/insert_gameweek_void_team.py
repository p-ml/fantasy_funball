import django
django.setup()


from fantasy_funball.models import Team


def insert_gameweek_void_team():
    """Insert a 'Gameweek Void' team to represent postponed
    matches"""
    gameweek_void = Team(team_name="Gameweek Void")
    gameweek_void.save()


if __name__ == "__main__":
    insert_gameweek_void_team()
